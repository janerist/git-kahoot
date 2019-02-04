# git-kahoot
Generate Kahoot quiz from commits in a git repository.

## Installation

Requires Python 3.
```
pip install git-kahoot
```

## Usage
```
Usage: git-kahoot [OPTIONS]

  Generate a Kahoot quiz from commits in a git repository.

Options:
  -d, --directory DIRECTORY       path to git repository (default: current
                                  directory) Specify this option multiple
                                  times to use multiple repositories.
  --since [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  only include commits since this date
  --until [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  only include commits up until this date
  -n, --count INTEGER RANGE       number of questions (default: 20, max: 100)
  -u, --username TEXT             Kahoot user name  [required]
  -p, --password TEXT             Kahoot password  [required]
  -t, --title TEXT                title of the generated quiz (default: "Git
                                  Commiter Quiz"
  --help                          Show this message and exit.
```

## Examples

Specify path to git repository using the -d option. Omitting this options will try to use the current directory.
```
git-kahoot --directory /my/repo
```

Multiple git repositories can be specfied. Commits will be selected in a round-robin fashion.
```
git-kahoot --directory /my/repo --directory /my/second-repo
```

Only include commits between a date range.
```
git-kahoot --directory /my/repo --since 2015-01-01 --until 2018-01-01
```

Set the title of the generated quiz and the number of questions.
```
git-kahoot --title "My glorious quiz" --count 10
```

Specify credentials for your Kahoot account. You will be prompted for these credentials if you omit them.
```
git-kahoot --username AzureDiamond --password hunter2
```

## Development setup

Assuming Python 3, pip and virtualenv is installed, clone the repository, set up a virtualenv and install the package as editable. 

```
git clone git@github.com:janerist/git-kahoot.git
cd git-kahoot
virtualenv -p python3 venv
. venv/bin/activate (Windows: venv/Scripts/activate)
pip install --editable .
git-kahoot
```
