import subprocess
import os


class GitError(Exception):
    pass


def get_git_dir(directory):
    try:
        git_dir = subprocess.check_output(
            ['git', 'rev-parse', '--git-dir'], universal_newlines=True, cwd=directory, stderr=subprocess.DEVNULL)
        return os.path.abspath(git_dir.strip())
    except subprocess.CalledProcessError:
        raise GitError(f'Directory "{directory}" not a git repository.')