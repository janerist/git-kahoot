import requests


KAHOOT_URL = 'https://create.kahoot.it/rest'


class KahootError(Exception):
    pass 


def authenticate(username, password):
    payload = {'username': username, 'password': password, 'grant_type': 'password'}
    response = requests.post(KAHOOT_URL + '/authenticate', json=payload)

    if response.status_code != requests.codes.ok:
        raise KahootError('Authentication failed. Did you type your password correctly?') 

    return response.json()['access_token']


def create_quiz(quiz, access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.post(KAHOOT_URL + '/kahoots', json=quiz, headers=headers)

    if response.status_code != requests.codes.ok:
        raise KahootError('Failed to create quiz. The response was: ' + response.json()) 

    return response.json()['uuid']
