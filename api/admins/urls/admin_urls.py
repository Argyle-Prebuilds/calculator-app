from admins.views.admin_users_views import CreateAdminUser, DeleteAdminUser, GetAdminUsers, ActivateAdminUser
from django.urls import path

urlpatterns = [
    path('create/', CreateAdminUser.as_view()),
    path('list/', GetAdminUsers.as_view()),
    path('delete/<uuid:pk>/', DeleteAdminUser.as_view()),
    path('activate/<uuid:pk>/', ActivateAdminUser.as_view()),
]

