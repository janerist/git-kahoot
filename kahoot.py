class KahootError(Exception):
    pass


def authenticate(username, password):
    raise KahootError('Invalid username and/or password')