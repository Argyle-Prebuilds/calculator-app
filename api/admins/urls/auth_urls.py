from admins.views.auth_views import LoginView, PasswordUpdateView, PasswordResetSendMailView, ValidateTokenView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('password-reset/', PasswordResetSendMailView.as_view()),
    path('password-update/', PasswordUpdateView.as_view()),
    path('validate-token/', ValidateTokenView.as_view()),
]
