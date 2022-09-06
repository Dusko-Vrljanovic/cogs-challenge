from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from account.factory import UserFactory
from quiz.models import Quiz, Question, Answer


class QuizFactory(DjangoModelFactory):
    title = Faker('pystr')
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Quiz


class QuestionFactory(DjangoModelFactory):
    quiz = SubFactory(QuizFactory)
    text = Faker('pystr')

    class Meta:
        model = Question


class AnswerFactory(DjangoModelFactory):
    question = SubFactory(QuestionFactory)
    text = Faker('pystr')

    class Meta:
        model = Answer
