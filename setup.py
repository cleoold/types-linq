from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='types-linq',
    version='v0.2.1',
    url='https://github.com/cleoold/types-linq',
    license='BSD 2-Clause License',
    author='cleoold',
    description='Standard sequence helper methods with full typing support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['types_linq', 'types_linq.more'],
    package_data={
        '': ['*.pyi', 'py.typed'],
    },
    zip_safe=False,
    python_requires='>=3.7',
    extras_require={':python_version<"3.8"': ['typing_extensions']},
    platforms='any',
    classifiers=[
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Typing :: Typed',
    ],
)
