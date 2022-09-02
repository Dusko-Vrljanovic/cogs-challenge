from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)

from api.mixins import LoggedUserMixin, GetObjectMixin


class APIListView(LoggedUserMixin, ListAPIView):
    model = None

    def get_queryset(self):
        if self.model:
            return self.model.objects.all()

        return None


class APICreateView(LoggedUserMixin, CreateAPIView):
    pass


class APIRetrieveView(LoggedUserMixin, GetObjectMixin, RetrieveAPIView):
    pass


class APIUpdateView(LoggedUserMixin, GetObjectMixin, UpdateAPIView):
    pass


class APIDestroyView(LoggedUserMixin, GetObjectMixin, DestroyAPIView):
    pass


class APIListCreateView(APIListView, APICreateView):
    pass


class APIRetrieveUpdateView(APIRetrieveView, APIUpdateView):
    pass
