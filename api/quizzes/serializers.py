from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import User
from api.users.serializers import SimpleUserSerializer
from quiz.models import Quiz, Answer, Question


class QuizListSerializer(serializers.ModelSerializer):
    created_by = SimpleUserSerializer()

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'description',
            'created_by',
            'created_at',
            'questions_count',
            'final'
        )


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            'title',
            'description'
        )

    def create(self, validated_data):
        user = self.context['user']
        validated_data['created_by'] = user

        return super().create(validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'text'
        )


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'text',
            'is_correct'
        )


class CreateQuestionSerializer(serializers.ModelSerializer):
    answers = CreateAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'text',
            'answers'
        )

    def save(self):
        validated_data = self.validated_data
        answers = list()
        has_correct_answer = False
        validated_answers = validated_data.pop('answers', list())

        question = Question(
            **validated_data,
            quiz=self.context['quiz'],
            order_number=self.context['quiz'].questions_count
        )

        for answer in validated_answers:
            answers.append(Answer(**answer, question=question))
            if answer.get('is_correct'):
                has_correct_answer = True

        if not has_correct_answer:
            raise ValidationError({
                'answers': _('You have to have at least one correct answer')
            })

        question.save()
        Answer.objects.bulk_create(answers)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'order_number',
            'text',
            'is_multiple_choice',
            'answers'
        )


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'description',
            'final',
            'questions'
        )
