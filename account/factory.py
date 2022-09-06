from factory import (
    LazyFunction,
    Faker
)
from factory.django import DjangoModelFactory

from account.models import User
from cogs_quiz.factory import fake_username, fake_email


class UserFactory(DjangoModelFactory):
    username = LazyFunction(fake_username)
    email = LazyFunction(fake_email)
    password = 'password'
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = User
