import ast
import os
import re
from itertools import chain
from dataclasses import dataclass
from textwrap import dedent, indent
from typing import Any, Optional, Union

import api_spec


LINK_PREFIX = 'apiref.'


@dataclass
class MyParam:
    name: str
    tp: str
    default: Optional[str]

    def decl(self):
        if self.default is None:
            return self.name
        return f'{self.name}={self.default}'


@dataclass
class MyMethodDef:
    name: str
    tparams: list[str]
    params: list[MyParam]
    kwonlyparams: list[MyParam]
    self_type: str
    return_type: str
    comment: str
    is_static: bool
    is_abstract: bool

    def markdown(self):
        builder = ['#### ']
        if self.is_abstract:
            builder.append('abstract ')
        if self.is_static:
            builder.append('staticmethod ')
        else:
            builder.append('instancemethod ')
        builder.append(f'`{self.name}')
        if self.tparams:
            builder.append(f'[{", ".join(t for t in self.tparams)}]')
        builder.append('(')
        builder.append(', '.join(p.decl() for p in self.params))
        if self.kwonlyparams:
            if not self.params:
                builder.append('*, ')
            elif self.params and self.params[-1].name.startswith('*'):
                builder.append(', ')
            elif self.params:
                builder.append(', *, ')
        for p in self.kwonlyparams:
            builder.append(', '.join(p.decl() for p in self.kwonlyparams))
        builder.append(')`\n\n')

        builder = [''.join(builder)]

        if self.self_type:
            builder.append('Constraint\n')
            builder.append(f'  ~ *self*: {rewrite_code_with_links(self.self_type)}\n\n')

        if self.params or self.kwonlyparams:
            builder.append('Parameters\n')
        for p in chain(self.params, self.kwonlyparams):
            builder.append(f'  ~ *{p.name}*: {rewrite_code_with_links(p.tp)}\n')
        builder.append('\n')

        builder.append('Returns\n')
        builder.append(f'  ~ {rewrite_code_with_links(self.return_type)}\n\n')
        builder.append(f'{self.comment}\n\n')
        return ''.join(builder)


@dataclass
class MyPropertyDef:
    name: str
    return_type: str
    comment: str

    def markdown(self):
        builder = []
        builder.append(f'#### instanceproperty `{self.name}`\n\n')

        builder.append('Returns\n')
        builder.append(f'  ~ {rewrite_code_with_links(self.return_type)}\n\n')
        builder.append(f'{self.comment}\n\n')
        return ''.join(builder)


@dataclass
class MyClassDef:
    name: str
    tparams: list[str]
    bases: list[str]
    comment: str
    methods: list[MyMethodDef]
    properties: list[MyPropertyDef]

    def typename(self):
        builder = [self.name]
        if self.tparams:
            builder.append(f'[{", ".join(self.tparams)}]')
        return ''.join(builder)

    def markdown(self):
        builder = []
        builder.append(f'({LINK_PREFIX}{self.name})=\n')
        builder.append(f'## class `{self.typename()}`\n\n')

        builder.append(f'{self.comment}\n\n')

        builder.append('### Bases\n\n')
        for base in self.bases:
            builder.append(f'- {rewrite_code_with_links(base)}\n')
        builder.append('\n')

        builder.append(title := '### Members\n\n')
        for method in chain(self.properties, self.methods):
            builder.append(method.markdown())
            builder.append('---\n\n')
        if builder[-1] == '---\n\n' or builder[-1] == title:
            builder.pop()
        return ''.join(builder)


@dataclass
class MyVariableDef:
    name: str
    comment: str
    value: str  # currently module constants are only used as type variables... so value is fine

    def markdown(self):
        builder = []
        builder.append(f'({LINK_PREFIX}{self.name})=\n')
        builder.append(f'### `{self.name}`\n\n')
        builder.append('Equals\n')
        builder.append(f'  ~ {rewrite_code_with_links(self.value)}\n\n')
        builder.append(f'{self.comment}\n\n')
        return ''.join(builder)


class ModuleVisitor(ast.NodeVisitor):
    def __init__(self, mspec: api_spec.ModuleSpec) -> None:
        super().__init__()
        self.mspec = mspec
        self.module_string = ''
        self.global_vars: list[MyVariableDef] = []
        self.classes: list[MyClassDef] = []

        self.found_gvs: set[str] = {*()}
        self.found_classes: set[str] = {*()}

    def visit_root(self, root: ast.Module):
        # the first node may be a docstring
        if doc := get_def_docstring(root):
            self.module_string = rewrite_comments(doc)

        # report assignments (with trailing docstring)
        for i in range(len(root.body)):
            if isinstance(assign := root.body[i], ast.Assign):
                doc = ''
                if i + 1 < len(root.body) and (s := node_is_constant_str(root.body[i + 1])):
                    doc = s
                self.visit_Assign_with_doc_non_override(assign, doc)

        # report classes
        classdefs = (c for c in root.body if isinstance(c, ast.ClassDef))
        for classdef in classdefs:
            self.visit_ClassDef(classdef)

    def visit_Assign_with_doc_non_override(self, assign: ast.Assign, doc: str):
        assert len(assign.targets) == 1
        target = assign.targets[0]
        assert isinstance(target, ast.Name)
        name = target.id
        print(f'  Found assignment {name}')
        self.found_gvs.add(name)
        if name not in self.mspec['gvs']:
            return
        
        self.global_vars.append(MyVariableDef(
            name=name,
            comment=rewrite_comments(doc),
            value=ast.unparse(assign.value),
        ))


    # top level class definition
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        classname = node.name
        print(f'  Found class {classname}')
        self.found_classes.add(classname)
        if classname not in self.mspec['classes']:
            return

        classspec = self.mspec['classes'][classname]

        class_tparams = get_tparam_for_class(node)
        classdef = MyClassDef(
            name=classname,
            tparams=class_tparams,
            bases=[ast.unparse(n) for n in node.bases],
            comment=rewrite_comments(get_def_docstring(node)),
            methods=[],
            properties=[],
        )

        found_funnames = {*()}

        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                defname = stmt.name
                print(f'    Found def {defname}()')
                found_funnames.add(defname)
                if defname in classspec['methods']:
                    classdef.methods.append(get_method(stmt, class_tparams))
                if defname in classspec['readonly_properties']:
                    classdef.properties.append(get_property(stmt))

        enabled_funnames = set(m.name for m in chain(classdef.methods, classdef.properties))
        print(f'    STAT Found defs - enabled defs: {psetdiff(found_funnames, enabled_funnames)}')
        print(f'    STAT Enabled defs - found defs: {psetdiff(enabled_funnames,found_funnames)}')
        self.classes.append(classdef)

    # such logging is necessary to check which symbols should be exposed but forgotten in api_spec.py,
    # or vice versa
    def report_found_globals(self):
        enabled_varnames = set(a.name for a in self.global_vars)
        print(f'  STAT Found gvs - enabled vars: {psetdiff(self.found_gvs, enabled_varnames)}')
        print(f'  STAT Enabled gvs - found vars: {psetdiff(enabled_varnames, self.found_gvs)}')
        enabled_classnames = set(c.name for c in self.classes)
        print(f'  STAT Found classes - enabled classes: {psetdiff(self.found_classes, enabled_classnames)}')
        print(f'  STAT Enabled classes - found classes: {psetdiff(enabled_classnames, self.found_classes)}')


def psetdiff(a: set[str], b: set[str]):
    s = ', '.join(a - b)
    return f'{{{s}}}'


def get_method(fun_def: ast.FunctionDef, class_tparams: list[str]):
    # class tparam is not part of method's tparam
    is_static = find_decorator(fun_def, 'staticmethod')

    pos_args = [MyParam(
        name=arg.arg,
        tp=ast.unparse(arg.annotation) if arg.annotation else '',
        default=None,
        ) for arg in fun_def.args.args
    ]

    # fill in default vals for pos args
    if defaults := fun_def.args.defaults:
        for default, arg in zip(reversed(defaults), reversed(pos_args)):
            arg.default = ast.unparse(default)

    # remove self from args if not static and not constrained
    self_type = ''
    if not is_static and pos_args[0].name == 'self':
        self_type = pos_args[0].tp or ''
        del pos_args[0]

    # vaarg to the end of args
    if vaarg := fun_def.args.vararg:
        pos_args.append(MyParam(
            name=f'*{vaarg.arg}',
            tp=ast.unparse(vaarg.annotation),
            default=None,
        ))

    kwonlyargs = [MyParam(
        name=arg.arg,
        tp=ast.unparse(arg.annotation) if arg.annotation else '',
        default=None,
        ) for arg in fun_def.args.kwonlyargs
    ]

    # fill in default vals for kwonlyargs
    if kw_defaults := fun_def.args.kw_defaults:
        for default, arg in zip(reversed(kw_defaults), reversed(kwonlyargs)):
            arg.default = ast.unparse(default) if default else None

    return MyMethodDef(
        name=fun_def.name,
        tparams=get_tparam_for_method(fun_def, class_tparams),
        params=pos_args,
        kwonlyparams=kwonlyargs,
        self_type=self_type,
        return_type=ast.unparse(fun_def.returns),
        comment=rewrite_comments(get_def_docstring(fun_def)),
        is_static=is_static,
        is_abstract=find_decorator(fun_def, 'abstractmethod'),
    )


def get_property(fun_def: ast.FunctionDef):
    return MyPropertyDef(
        name=fun_def.name,
        return_type=ast.unparse(fun_def.returns),
        comment=rewrite_comments(get_def_docstring(fun_def)),
    )


def node_is_constant_str(node: ast.AST):
    if isinstance(node, ast.Expr) and \
        isinstance(const := node.value, ast.Constant) and \
        isinstance(s := const.value, str):
        return s
    return ''


def get_def_docstring(any_def: Union[ast.FunctionDef, ast.ClassDef, ast.Module]):
    return node_is_constant_str(any_def.body[0])


def find_decorator(any_def: Union[ast.FunctionDef, ast.ClassDef], name: str):
    return any(d.id == name for d in any_def.decorator_list)


class TParamFinder(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.tparams = []

    def visit_Name(self, node: ast.Name) -> Any:
        if is_tparam(node.id) and node.id not in self.tparams:
            self.tparams.append(node.id)


def get_tparam_for_class(class_def: ast.ClassDef):
    v = TParamFinder()
    for expr in class_def.bases:
        v.visit(expr)
    return v.tparams


def get_tparam_for_method(fun_def: ast.FunctionDef, class_tparams: list[str]):
    v = TParamFinder()
    v.visit(fun_def.args)
    tparams = [p for p in v.tparams if p not in class_tparams]
    return tparams


def rewrite_comments(s: str):
    s = dedent(s).strip()
    # rewrite the code Example blocks from markdown to myst's deflist
    eight = ' ' * 8
    s = re.sub(
        r'^Example\s```(.*?)\n(.*?)```$',
        lambda mat: f'Example\n    ~   ```{mat.group(1)}\n{indent(mat.group(2), eight)}{eight}```',
        s,
        flags=re.DOTALL | re.MULTILINE,
    )
    # rewrite code literals with their links if possible
    return re.sub(
        r'`([^\d\W][\w\d]*?)`',
        lambda mat: f'[`{name}`]({LINK_PREFIX}{name})' \
            if (name := mat.group(1)) in linkable_items else mat.group(0),
        s,
    )


def rewrite_code_with_links(code: str):
    identifier_regex = r'([^\d\W][\w\d]*)'  # not robust but sufficient for now
    builder = []
    continueable = False
    for seg in re.split(identifier_regex, code):
        if not seg:
            continue
        if seg in linkable_items:
            builder.append(f'[`{seg}`]({LINK_PREFIX}{seg})')
            continueable = False
        elif continueable:
            builder[-1] = f'{builder[-1][:-1]}{seg}`'
        else:
            builder.append(f'`{seg}`')
            continueable = True
    return ''.join(builder)


linkable_items = {*()}
tparams = {*()}

def is_tparam(s: str):
    return s in tparams


# fill in hyperlinkable items and project tparams
for module in api_spec.modules:
    if module['file_path'] == api_spec.type_file:
        tparams.update(v for v in module['gvs'] if v.startswith('T'))
    linkable_items.update(module['gvs'])
    linkable_items.update(module['classes'].keys())

# write api markdown for each module
for module in api_spec.modules:
    m_name = module['name']
    print(f'Processing module {m_name}')
    # if module name is more than one dot -> then the front ones means a submodule.
    # create nested folder
    sub_folder = ''
    if m_name.count('.') > 1:
        sub_folder = re.search(r'^\w+\.(.+)\.\w+$', m_name).group(1).replace('.', '/')
    os.makedirs(f'api/{sub_folder}', exist_ok=True)
    with open(module['file_path']) as fin, open(f'api/{sub_folder}/{m_name}.md', 'w') as fout:
        code = fin.read()
        v = ModuleVisitor(module)
        v.visit_root(ast.parse(code))
        v.report_found_globals()

        fout.write(f'# module ``{m_name}``\n\n')

        if v.module_string:
            fout.write(f'{v.module_string}\n\n')

        if v.global_vars:
            fout.write('## Constants\n\n')
            for i, var in enumerate(v.global_vars):
                fout.write(var.markdown())
                if i < len(v.global_vars) - 1:
                    fout.write('---\n\n')
            if v.classes:
                fout.write('---\n\n')

        for i, c in enumerate(v.classes):
            fout.write(c.markdown())
            if i < len(v.classes) - 1:
                fout.write('---\n\n')
