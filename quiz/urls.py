from django.urls import path, include

from quiz import views
from quiz.api import questions, categories

api_patterns = [
    path('get_questions/', questions.GetQuestionsView.as_view(), name='quiz.api.get_questions'),
    path('check_answers/', questions.CheckAnswersView.as_view(), name='quiz.api.check_answers'),
    path(
        'category_autocomplete/',
        categories.CategoriesAutocomplete.as_view(),
        name='quiz.api.category_autocomplete'
    ),
]

urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('api/quiz/', include(api_patterns)),
]