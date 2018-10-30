import subprocess
import os


class GitError(Exception):
    pass


def get_git_dir(directory):
    try:
        git_dir = subprocess.check_output(
            ['git', 'rev-parse', '--git-dir'], 
            universal_newlines=True, 
            cwd=directory, 
            stderr=subprocess.DEVNULL
        )

        if os.path.isabs(git_dir):
            return git_dir.strip()

        return os.path.join(os.path.abspath(directory), git_dir.strip())

    except subprocess.CalledProcessError:
        raise GitError(f'Directory "{directory}" not a git repository.')


def get_authors(directory):
    authors = subprocess.check_output(
        ['git', 'log', '--format="%an"'],
        universal_newlines=True,
        cwd=directory
    )

    return set([author.strip('\"') for author in authors.splitlines()])


def get_random_commits(directory, since, until, count):
    pass