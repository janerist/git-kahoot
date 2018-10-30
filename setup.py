from setuptools import setup

setup(
    name='git-kahoot',
    version='0.1',
    py_modules=['git_kahoot'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        git-kahoot=git_kahoot:cli
    ''',
)