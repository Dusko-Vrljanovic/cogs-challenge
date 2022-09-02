# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.serializers import UserRegisterSerializer, UserDetailsSerializer
from api.views import APICreateView, APIRetrieveView


class UserRegisterView(APICreateView):
    permission_classes = (AllowAny, )
    serializer_class = UserRegisterSerializer


class UserDetailsView(APIRetrieveView):
    serializer_class = UserDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        # return Response(UserDetailsSerializer(instance=instance).data)
