from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='git-kahoot',
    version='0.2.3',
    author='Jan-Erik Strøm',
    author_email='jan.erik.strom@gmail.com',
    description='Generate a Kahoot quiz from commits in a git repository',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/janerist/git-kahoot',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['cli', 'git', 'kahoot'],
    install_requires=[
        'Click==8.0.1',
        'requests==2.31.0'
    ],
    entry_points='''
        [console_scripts]
        git-kahoot=cli:cli
    ''',
)
