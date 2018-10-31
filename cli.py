import click
import subprocess
import os
import kahoot
import git
import random
from itertools import islice, cycle

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
@click.option('-t', '--title', default='Git Commiter Quiz', help='title of the generated quiz')
def cli(directory, since, until, count, username, password, title):
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

    click.echo('Getting commits...')

    authors = git.get_authors(directory)
    commits = git.get_random_commits(directory, since, until, count)

    click.echo('Creating quiz...')

    questions = [create_question(commit, authors) for commit in commits] 

    quiz = {
        'title': title,
        'description': 'Made using git-kahoot',
        'type': 'quiz',
        'quizType': 'quiz',
        'language': 'English',
        'audience': 'Social',
        'coverMetadata': {},
        'questions': questions
    }

    quiz_id = kahoot.create_quiz(quiz, access_token)

    click.echo(f'Success! Your quiz is ready at: https://play.kahoot.it/#/?quizId={quiz_id}')


def create_question(commit, authors):
    author, date, message = commit
    choices = [] 
    if len(authors) < 4:
        choices.extend(list(islice(cycle(authors), None, 4)))
    else:
        choices.extend(random.sample(authors, 4))

    if not author in choices:
        choices.pop()
        choices.append(author)

    random.shuffle(choices)

    return {
        'question': message,
        'questionFormat': 0,
        'time': 20000,
        'points': True,
        'numberOfAnswers': len(choices),
        'image': '',
        'imageMetadata': {},
        'resources': '',
        'video': {
            'id': '',
            'startTime': 0,
            'endTime': 0,
            'service': 'youtube',
            'fullUrl': ''
        },
        'choices': [{'answer': choice, 'correct': choice == author} for choice in choices]
    }
