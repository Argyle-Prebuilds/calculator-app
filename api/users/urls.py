from django.urls import path

from .views import ArgyleUsersListCreate, ArgyleUsersDelete

urlpatterns = [
    path('', ArgyleUsersListCreate.as_view()),
    path('<uuid:argyle_user_id>', ArgyleUsersDelete.as_view()),
]
