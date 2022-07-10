import ast
import os
import re
from itertools import chain
from dataclasses import dataclass
from textwrap import dedent, indent
from typing import Any, Optional, Union

import api_spec


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

    def markdown(self):
        builder = ['#### ']
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
            builder.append(f'  ~ *self*: `{self.self_type}`\n\n')

        if self.params or self.kwonlyparams:
            builder.append('Parameters\n')
        for p in chain(self.params, self.kwonlyparams):
            builder.append(f'  ~ *{p.name}* (`{p.tp}`)\n')
        builder.append('\n')

        builder.append('Returns\n')
        builder.append(f'  ~ `{self.return_type}`\n\n')
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
        builder.append(f'  ~ `{self.return_type}`\n\n')
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
        builder.append(f'## class `{self.typename()}`\n\n')

        builder.append(f'{self.comment}\n\n')

        builder.append('### Bases\n\n')
        for base in self.bases:
            builder.append(f'- `{base}`\n')
        builder.append('\n')

        builder.append(title := '### Members\n\n')
        for method in chain(self.properties, self.methods):
            builder.append(method.markdown())
            builder.append('---\n\n')
        if builder[-1] == '---\n\n' or builder[-1] == title:
            builder.pop()
        return ''.join(builder)


class ModuleVisitor(ast.NodeVisitor):
    def __init__(self, mspec: api_spec.ModuleSpec) -> None:
        super().__init__()
        self.mspec = mspec
        self.classes: list[MyClassDef] = []

        self.found_classes: set[str] = {*()}

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
            comment=rewrite_comments(get_docstring(node)),
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
        comment=rewrite_comments(get_docstring(fun_def)),
        is_static=is_static,
    )


def get_property(fun_def: ast.FunctionDef):
    return MyPropertyDef(
        name=fun_def.name,
        return_type=ast.unparse(fun_def.returns),
        comment=rewrite_comments(get_docstring(fun_def)),
    )


def get_docstring(any_def: Union[ast.FunctionDef, ast.ClassDef]):
    docstring = ''
    if any_def.body and isinstance(any_def.body[0], ast.Expr) and \
        isinstance(const := any_def.body[0].value, ast.Constant) and \
        isinstance(const.value, str):
        docstring = const.value
    return docstring


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
    return re.sub(
        r'^Example\s```(.*?)\n(.*?)```$',
        lambda mat: f'Example\n    ~   ```{mat.group(1)}\n{indent(mat.group(2), eight)}{eight}```',
        s,
        flags=re.DOTALL | re.MULTILINE,
    )

tparams = {*()}

def is_tparam(s: str):
    return s in tparams


# fill in project tparams
with open(api_spec.type_file) as f:
    class _(ast.NodeVisitor):
        def visit_Assign(self, node: ast.Assign) -> Any:
            name = node.targets[0].id
            if isinstance(node.value, ast.Call) and node.value.func.id == 'TypeVar':
                tparams.add(name)
    _().visit(ast.parse(f.read()))

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
        v.visit(ast.parse(code))
        v.report_found_globals()

        fout.write(f'# module ``{m_name}``\n\n')

        for i, c in enumerate(v.classes):
            fout.write(c.markdown())
            if i < len(v.classes) - 1:
                fout.write('---\n\n')
