from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.quizzes.serializers import QuestionSerializer
from quiz.models import Quiz
from quiz_attempt.models import QuizAttempt, QuizAttemptAnswers


class ListQuizzesSerializer(serializers.ModelSerializer):

    best_score = serializers.SerializerMethodField()
    last_score = serializers.SerializerMethodField()
    total_attempts = serializers.SerializerMethodField()
    current_run = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'description',
            'questions_count',
            'best_score',
            'last_score',
            'total_attempts',
            'current_run'
        )

    def get_best_score(self, quiz: Quiz):
        best_attempt = quiz.get_best_score(self.context['user'])

        return best_attempt.score if best_attempt else None

    def get_last_score(self, quiz: Quiz):
        last_attempt = quiz.get_last_score(self.context['user'])

        return last_attempt.score if last_attempt else None

    def get_total_attempts(self, quiz: Quiz):
        return quiz.get_user_attempts(self.context['user']).count()

    def get_current_run(self, quiz: Quiz):
        current_run = quiz.get_current_run(self.context['user'])

        return dict(
            answer_count=current_run.answered_questions,
            in_progress=True
        ) if current_run else None


class QuizAttemptSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'questions',
            'answers'
        )

    def get_answers(self, quiz: Quiz):
        current_run = quiz.get_current_run(self.context['user'])

        if not current_run:
            return None

        return {
            question_answer.question.id: question_answer.answers
            for question_answer in current_run.quiz_answers.all()
        }


class SubmitQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )


class SubmitQuizSerializer(serializers.Serializer):
    questions = SubmitQuestionSerializer(many=True)

    def validate_questions_and_answers(self, validated_data, quiz_questions):
        questions_and_answers = dict()
        for question in validated_data['questions']:
            if question['id'] not in quiz_questions:
                raise ValidationError(
                    _('Invalid questions ids')
                )

            question_answers = set(question['answers'])
            if question_answers - quiz_questions[question['id']]['answers']:
                raise ValidationError(
                    _('Invalid answer ids')
                )

            questions_and_answers[question['id']] = question['answers']

        return questions_and_answers

    def perform_update_in_db(
            self,
            questions_and_answers_data,
            db_data,
            current_run
    ):
        current_run: QuizAttempt
        score = 0
        answered_questions = len(questions_and_answers_data.keys())
        for question in current_run.quiz_answers.all():
            if question.id not in questions_and_answers_data:
                question.delete()
            else:
                question.answers = questions_and_answers_data[question.id]
                questions_and_answers_data.pop(question.id, None)

        for question_id, answers in questions_and_answers_data.items():
            QuizAttemptAnswers(
                quiz_attempt=current_run,
                question=db_data[question_id]['question'],
                answers=answers
            ).save()

            if set(answers) == db_data[question_id]['correct_answers']:
                score += 1

        current_run.answered_questions = answered_questions
        finish_attempt = self.context.get('finish_attempt', False)
        if finish_attempt:
            current_run.score = score
            current_run.finished_at = now()
        current_run.save()

    def update(self, instance, validated_data):
        instance: Quiz
        current_run = instance.get_current_run(self.context['user'])
        if not current_run:
            raise ValidationError(
                _('There is no active attempt')
            )
        
        db_quiz_questions = instance.question_and_answer_ids
        question_and_answers_data = self.validate_questions_and_answers(
            validated_data,
            db_quiz_questions
        )
        with transaction.atomic():
            self.perform_update_in_db(
                question_and_answers_data,
                db_quiz_questions,
                current_run
            )

        return instance


        
