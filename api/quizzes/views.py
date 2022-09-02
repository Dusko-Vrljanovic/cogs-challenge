from django.shortcuts import render

# Create your views here.
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

from api.views import (
    APIListCreateView,
    APICreateView,
    APIRetrieveUpdateView,
    APIUpdateView,
    APIDestroyView,
)
from quiz.models import Quiz, Question

from .serializers import (
    QuizCreateSerializer,
    QuizListSerializer,
    QuizSerializer, CreateQuestionSerializer
)
from ..mixins import QuizRelatedMixin


class ListCreateView(APIListCreateView):
    model = Quiz

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuizCreateSerializer

        return QuizListSerializer


class RetrieveUpdateView(APIRetrieveUpdateView):
    model = Quiz

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuizSerializer

        return QuizCreateSerializer

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_user_update(self.request.user.id):
            return Response(
                _('Only user that created quiz can update it'),
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            status=status.HTTP_200_OK,
            data=QuizListSerializer(instance=instance).data
        )


class AddQuestionView(QuizRelatedMixin, APICreateView):
    serializer_class = CreateQuestionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        quiz = self.get_serializer_context()['quiz']

        return Response(
            QuizSerializer(instance=quiz).data,
            status=status.HTTP_200_OK,
        )


class RemoveQuestionView(QuizRelatedMixin, APIDestroyView):
    model = Question

    def delete(self, request, *args, **kwargs):
        self.get_serializer_context()
        return self.destroy(request, *args, **kwargs)


class MakeQuizFinalView(QuizRelatedMixin, APIUpdateView):
    model = Quiz
    serializer_class = QuizSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = dict(final=True)
        serializer = self.get_serializer(
            instance, 
            data=data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
