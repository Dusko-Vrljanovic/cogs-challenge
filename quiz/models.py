from django.db import models

from django.utils.timezone import now


class Quiz(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField(default='')
    created_by = models.ForeignKey(
        'account.User',
        on_delete=models.DO_NOTHING,
        default=None
    )
    created_at = models.DateTimeField(default=now)
    final = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']
        db_table = 'quiz'

    def __str__(self):
        return self.title

    @property
    def questions_count(self):
        return self.questions.count()

    @property
    def question_and_answer_ids(self):
        quiz_questions = dict()
        for question in self.questions.all():
            answer_ids = set()
            correct_answer_ids = set()
            for answer in question.answers.all():
                answer_ids.add(answer.id)
                if answer.is_correct:
                    correct_answer_ids.add(answer.id)

            quiz_questions[question.id] = dict(
                question=question,
                answers=answer_ids,
                correct_answers=correct_answer_ids
            )

        return quiz_questions

    def can_user_update(self, user_id):
        return self.created_by.id == user_id

    def get_user_attempts(self, user):
        return self.attempts.filter(user=user)

    def get_current_run(self, user):
        return self.get_user_attempts(user).filter(
            finished_at__isnull=True
        ).first()

    def get_last_score(self, user):
        return self.get_user_attempts(user).filter(
            finished_at__isnull=False
        ).order_by('-started_at').first()

    def get_best_score(self, user):
        return self.get_user_attempts(user).filter(
            finished_at__isnull=False
        ).order_by('-score').first()


class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE
    )
    order_number = models.IntegerField()
    text = models.CharField(max_length=256)

    @property
    def is_multiple_choice(self):
        return self.answers.filter(is_correct=True).count() > 1

    def delete(self, using=None, keep_parents=False):
        questions = self.quiz.questions.filter(
            order_number__gt=self.order_number
        )
        for question in questions:
            question.order_number -= 1
            question.save()

        return super().delete()

    class Meta:
        ordering = ['order_number']
        db_table = 'question'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'answer'
