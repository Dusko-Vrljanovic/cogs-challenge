from factory import SubFactory
from factory.django import DjangoModelFactory

from account.factory import UserFactory
from quiz.factory import QuizFactory, QuestionFactory
from quiz_attempt.models import QuizAttempt, QuizAttemptAnswers


class QuizAttemptFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    quiz = SubFactory(QuizFactory)

    class Meta:
        model = QuizAttempt


class QuizAttemptAnswersFactory(DjangoModelFactory):
    quiz_attempt = SubFactory(QuizAttemptFactory)
    question = SubFactory(QuestionFactory)

    class Meta:
        model = QuizAttemptAnswers
