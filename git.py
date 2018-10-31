import subprocess
import os
import random
from itertools import islice, cycle


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
    commit_delimiter = 'XXXCOMMIT'
    field_delimiter = '|||'
    commit_format = field_delimiter.join(['%an', '%ar', '%B'])
    
    args = ['git', 'log', '--no-merges', f'--pretty="{commit_format}{commit_delimiter}"']
    if since is not None:
        args.append(f'--since={since}')
    if until is not None:
        args.append(f'--until={until}')

    output = subprocess.check_output(
        args,
        universal_newlines=True,
        cwd=directory
    )

    raw_commits = output.split(commit_delimiter)[:-1]
    if len(raw_commits) < count:
        raw_commits = list(islice(cycle(raw_commits), None, count))

    random_commits = random.sample(raw_commits, count)
    commits = []
    for commit in random_commits:
        fields = commit.strip().split(field_delimiter)
        commits.append((fields[0].strip('[\n\"]'), fields[1], fields[2]))

    return commits

    


