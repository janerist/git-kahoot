from setuptools import setup

setup(
    name='git-kahoot',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        git-kahoot=cli:cli
    ''',
)