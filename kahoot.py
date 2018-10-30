import requests


KAHOOT_URL = 'https://create.kahoot.it/rest'


class KahootError(Exception):
    pass 


def authenticate(username, password):
    payload = {'username': username, 'password': password, 'grant_type': 'password'}
    response = requests.post(f'{KAHOOT_URL}/authenticate', json=payload)

    if response.status_code != requests.codes.ok:
        raise KahootError('Authentication failed. Did you type your password correctly?') 

    return response.json()['access_token']