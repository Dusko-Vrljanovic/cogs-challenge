from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.ListCreateView.as_view(), name='list'),
    path('<int:object_id>/', views.RetrieveUpdateView.as_view(), name='update'),
    path('<int:quiz_id>/add-question/',
         views.AddQuestionView.as_view(), name='add-question'),
    path('<int:quiz_id>/remove-question/<int:object_id>/',
         views.RemoveQuestionView.as_view(), name='remove-question'),
    path('<int:quiz_id>/finalize/',
         views.MakeQuizFinalView.as_view(), name='finalize')

]

