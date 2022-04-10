from django.urls import path

from custom_auth.api import authorization

urlpatterns = [
    path('', authorization.AuthView.as_view(), name='auth.api.auth'),
]
