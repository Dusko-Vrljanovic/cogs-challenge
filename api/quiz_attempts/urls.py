from django.urls import path

from . import views

app_name = 'quiz-attempts'

urlpatterns = [
    path('', views.ListView.as_view(), name='list'),
    path('attempt/<int:quiz_id>/',
         views.AttemptQuizView.as_view(), name='attempt'),
    path('submit/<int:quiz_id>/',
         views.SubmitQuizView.as_view(), name='submit'),
    path('save-progress/<int:quiz_id>/',
         views.SaveQuizProgressView.as_view(), name='save-progress'),
]