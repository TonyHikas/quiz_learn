from django.urls import path
from quiz import views
from quiz.api import questions, categories

urlpatterns = [
    path('/', views.home_view, name='home_page'),
    path('api/get_questions/', questions.GetQuestionsView.as_view(), name='quiz.api.get_questions'),
    path('api/check_answers/', questions.CheckAnswersView.as_view(), name='quiz.api.check_answers'),
    path(
        'api/category_autocomplete/',
        categories.CategoriesAutocomplete.as_view(),
        name='quiz.api.category_autocomplete'
    ),
]
