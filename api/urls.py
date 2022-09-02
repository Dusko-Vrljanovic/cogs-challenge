from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('quizzes/administration/', include('api.quizzes.urls')),
    path('users/', include('api.users.urls')),
    path('quizzes/', include('api.quiz_attempts.urls'))
]
