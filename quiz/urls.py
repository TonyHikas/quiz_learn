from django.urls import path
from quiz import views
from quiz.api import questions

urlpatterns = [
    path('/', views.home_view, name='home_page'),
    path('get_questions/', questions.GetQuestionsView.as_view(), name='quiz.api.get_questions'),
    path('check_answers/', questions.CheckAnswersView.as_view(), name='quiz.api.check_answers'),
]