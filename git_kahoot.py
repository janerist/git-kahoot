import click
import subprocess
from subprocess import CalledProcessError
import os


def validate_git_repo(ctx, param, value):
    try:
        git_dir = subprocess.check_output(
            ['git', 'rev-parse', '--git-dir'], universal_newlines=True, cwd=value, stderr=subprocess.DEVNULL)
        return os.path.abspath(git_dir.strip())
    except CalledProcessError:
        raise click.BadParameter(
            f'Directory "{value}" not a git repository.')


@click.command()
@click.option('-d', '--directory', default='.', help='path to git repository (default: current directory)',
              type=click.Path(exists=True, file_okay=False), callback=validate_git_repo)
@click.option('--since', help='only include commits since this date', type=click.DateTime())
@click.option('--until', help='only include commits up until this date', type=click.DateTime())
@click.option('-n', '--count', default=20, help='number of questions (default: 20, max: 100)',
              type=click.IntRange(min=1, max=100))
def cli(directory, since, until, count):
    """Generates Kahoot quiz from commits in a git repository."""

    if since is not None and until is not None and since >= until:
        raise click.BadOptionUsage('until', '--until must be after --since')

    click.echo(f'Using git repository {directory}')
    if (since is not None):
        click.echo(f'Only including commits since {since}')
    if (until is not None):
        click.echo(f'Only including commits up to {until}')
    click.echo(f'Number of questions: {count}')
