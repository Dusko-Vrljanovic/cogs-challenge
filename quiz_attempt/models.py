from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from django.utils.timezone import now


class QuizAttempt(models.Model):

    user = models.ForeignKey(
        'account.User',
        on_delete=models.PROTECT,
        related_name='attempts'
    )

    quiz = models.ForeignKey(
        'quiz.Quiz',
        on_delete=models.PROTECT,
        related_name='attempts'
    )

    started_at = models.DateTimeField(default=now)
    finished_at = models.DateTimeField(blank=True, null=True)

    answered_questions = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'quiz_attempt'
        ordering = ['started_at']


class QuizAttemptAnswers(models.Model):
    quiz_attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.PROTECT,
        related_name='quiz_answers'
    )

    question = models.ForeignKey(
        'quiz.Question',
        on_delete=models.PROTECT,
        related_name='question_answers'
    )

    answers = ArrayField(models.IntegerField(), default=list, blank=True)
