from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from quiz.models import Quiz


class LoggedUserMixin(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['user'] = self.request.user
        return ctx


class GetObjectMixin(GenericAPIView):
    model = None

    def get_object(self):
        if self.model:
            if 'object_id' in self.kwargs:
                object_id = self.kwargs.get('object_id')
            else:
                object_id = self.kwargs.get('quiz_id')
            return get_object_or_404(self.model.objects.all(), id=object_id)

        return Response(_('Not found'), status=status.HTTP_404_NOT_FOUND)


class QuizRelatedMixin(GenericAPIView):
    def get_serializer_context(self):
        quiz_id = self.kwargs.get('quiz_id')
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if not quiz:
            raise ValidationError(_('Quiz not found'))
        
        if not quiz.can_user_update(self.request.user.id):
            raise ValidationError(
                _('Only user that created quiz can update it')
            )

        if quiz.final:
            raise ValidationError(
                _('Quiz cannot be updated after it is made final')
            )
        
        ctx = super().get_serializer_context()
        ctx['quiz'] = quiz
        return ctx
