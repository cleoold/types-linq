from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='types-linq',
    version='v0.0.1',
    url='https://github.com/cleoold/types-linq',
    license='GNU General Public License v3',
    author='cleoold',
    description='LINQ with full typing support (WIP).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['types_linq'],
    package_data={
        '': ['*.pyi', 'py.typed'],
    },
    zip_safe=False,
    python_requires='>=3.7',
    platforms='any',
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Typing :: Typed',
    ],
)
