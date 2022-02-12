from django.urls import path
from quiz import views

urlpatterns = [
    path('/', views.home_view, name='home_page'),
]