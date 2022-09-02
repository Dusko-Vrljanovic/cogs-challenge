# Create your views here.
from rest_framework.permissions import AllowAny

from api.users.serializers import UserRegisterSerializer
from api.views import APICreateView


class UserRegisterView(APICreateView):
    permission_classes = (AllowAny, )
    serializer_class = UserRegisterSerializer
