import click
import kahoot
import git
import random
from itertools import islice, cycle
import os


def validate_git_repo(ctx, param, repos):
    try:
        return [git.get_git_dir(repo) for repo in repos]
    except git.GitError as err:
        raise click.BadParameter(err)


@click.command()
@click.option(
    '-d',
    '--directory',
    'repos',
    default='.',
    multiple=True,
    help='path to git repository (default: current directory) Specify this option multiple times to use multiple repositories.',
    type=click.Path(exists=True, file_okay=False),
    callback=validate_git_repo
)
@click.option(
    '--since',
    help='only include commits since this date',
    type=click.DateTime()
)
@click.option(
    '--until',
    help='only include commits up until this date',
    type=click.DateTime()
)
@click.option(
    '-n',
    '--count',
    default=20,
    help='number of questions (default: 20, max: 100)',
    type=click.IntRange(min=1, max=100)
)
@click.option(
    '-u',
    '--username',
    required=True,
    prompt='Kahoot user name',
    help='Kahoot user name'
)
@click.option(
    '-p',
    '--password',
    required=True,
    prompt='Kahoot password',
    hide_input=True,
    help='Kahoot password'
)
@click.option(
    '-t',
    '--title',
    default='Git Commiter Quiz',
    help='title of the generated quiz (default: "Git Commiter Quiz"'
)
def cli(repos, since, until, count, username, password, title):
    """Generates Kahoot quiz from commits in a git repository."""

    if since is not None and until is not None and since >= until:
        raise click.BadOptionUsage('until', '--until must be after --since')

    try:
        access_token = kahoot.authenticate(username, password)
    except kahoot.KahootError as err:
        raise click.UsageError(err)

    for repo in repos:
        click.echo(f'Using git repository {repo}')
    if since is not None:
        click.echo(f'Only including commits since {since}')
    if until is not None:
        click.echo(f'Only including commits up to {until}')
    click.echo(f'Number of questions: {count}')

    click.echo('Getting commits...')

    repodata = [{'name': os.path.basename(os.path.abspath(os.path.join(repo, '..'))),
                 'authors': git.get_authors(repo),
                 'commits': git.get_random_commits(repo, since, until, count)} for repo in repos]

    questions = [create_question(repo['name'] if len(repos) > 1 else None, repo['authors'], repo['commits'].pop())
                 for repo in islice(cycle(repodata), None, count)]

    random.shuffle(questions)

    click.echo('Creating quiz...')

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


def create_question(repo_name, authors, commit):
    author, date, message = commit
    choices = []
    if len(authors) < 4:
        choices.extend(list(islice(cycle(authors), None, 4)))
    else:
        choices.extend(random.sample(authors, 4))

    if author not in choices:
        choices.pop()
        choices.append(author)

    random.shuffle(choices)

    question = f'[{repo_name}] ' if repo_name else ''
    question += f'({date}):\n{message}'

    return {
        'question': question,
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
