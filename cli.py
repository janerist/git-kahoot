import click
import subprocess
import os
import kahoot
import git

def validate_git_repo(ctx, param, value):
    try:
        return git.get_git_dir(value)
    except git.GitError as err:
        raise click.BadParameter(err)

@click.command()
@click.option('-d', '--directory', default='.', help='path to git repository (default: current directory)',
              type=click.Path(exists=True, file_okay=False), callback=validate_git_repo)
@click.option('--since', help='only include commits since this date', type=click.DateTime())
@click.option('--until', help='only include commits up until this date', type=click.DateTime())
@click.option('-n', '--count', default=20, help='number of questions (default: 20, max: 100)',
              type=click.IntRange(min=1, max=100))
@click.option('-u', '--username', required=True, prompt='Kahoot user name', help='Kahoot user name')
@click.option('-p', '--password', required=True, prompt='Kahoot password', hide_input=True, help='Kahoot password')
def cli(directory, since, until, count, username, password):
    """Generates Kahoot quiz from commits in a git repository."""

    if since is not None and until is not None and since >= until:
        raise click.BadOptionUsage('until', '--until must be after --since')

    try:
        access_token = kahoot.authenticate(username, password)
    except kahoot.KahootError as err:
        raise click.UsageError(err)

    click.echo(f'Using git repository {directory}')
    if (since is not None):
        click.echo(f'Only including commits since {since}')
    if (until is not None):
        click.echo(f'Only including commits up to {until}')
    click.echo(f'Number of questions: {count}')
    click.echo(f'Kahoot user name: {username}')
    click.echo(f'Kahoot access token: {access_token}')
