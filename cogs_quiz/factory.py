from uuid import uuid4


def fake_email():
    return f'{uuid4()}@cogs-quiz.com'


def fake_username():
    return f'{uuid4()}'
