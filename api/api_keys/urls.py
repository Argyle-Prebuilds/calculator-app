from django.urls import path

from .views import APIKeyListCreateView

urlpatterns = [
    path('api-keys/', APIKeyListCreateView.as_view()),
]
