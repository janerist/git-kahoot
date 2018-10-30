import click
import subprocess
from subprocess import CalledProcessError
import os


def validate_git_repo(ctx, param, value):
    try:
        git_dir = subprocess.check_output(
            ['git', 'rev-parse', '--git-dir'], universal_newlines=True, cwd=value, stderr=subprocess.DEVNULL)
        return os.path.abspath(git_dir)
    except CalledProcessError:
        raise click.BadParameter(
            f'Directory "{value}" not a git repository.')


@click.command()
@click.option('-d', '--directory', default='.', help='Path to git repository (default: current directory).',
              type=click.Path(exists=True, file_okay=False), callback=validate_git_repo
              )
def cli(directory):
    """Generates Kahoot quiz from commits in a git repository."""
    click.echo(f'Using git repository {directory}')
