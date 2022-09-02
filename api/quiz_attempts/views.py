from rest_framework.response import Response

from api.quiz_attempts.serializers import (
    ListQuizzesSerializer,
    QuizAttemptSerializer, 
    SubmitQuizSerializer
)
from api.views import APIListView, APIRetrieveView, APIUpdateView
from quiz.models import Quiz
from quiz_attempt.models import QuizAttempt


class ListView(APIListView):
    serializer_class = ListQuizzesSerializer
    
    def get_queryset(self):
        return Quiz.objects.prefetch_related('attempts').filter(final=True)


class AttemptQuizView(APIRetrieveView):
    model = Quiz
    serializer_class = QuizAttemptSerializer

    def get_object(self):
        self.kwargs['additional_kwargs'] = {
            'final': True
        }

        return super().get_object()

    def provide_current_run(self, quiz):
        user = self.request.user
        current_run = quiz.get_current_run(user)

        if not current_run:
            QuizAttempt.objects.create(
                user=user,
                quiz=quiz
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.provide_current_run(instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class SaveQuizProgressView(APIUpdateView):
    model = Quiz
    serializer_class = SubmitQuizSerializer
    
    def get_object(self):
        self.kwargs['additional_kwargs'] = {
            'final': True
        }

        return super().get_object()
    
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['finish_attempt'] = False
        return ctx
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        response_serializer = ListQuizzesSerializer(
            instance=instance,
            context=self.get_serializer_context()
        )
        return Response(response_serializer.data)


class SubmitQuizView(SaveQuizProgressView):
    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['finish_attempt'] = True
        return ctx
