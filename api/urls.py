from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('quizzes/', include('api.quizzes.urls')),
    path('users/', include('api.users.urls'))
]
