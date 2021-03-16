from django.urls import path

from .views import ArgyleUsersListCreate, ArgyleUsersDelete, KeyMetricsList, EmploymentList, ProfileView

urlpatterns = [
    path('', ArgyleUsersListCreate.as_view()),
    path('<uuid:argyle_user_id>', ArgyleUsersDelete.as_view()),
    path('<uuid:argyle_user_id>/key-metrics', KeyMetricsList.as_view(), name="key-metrics"),
    path('<uuid:argyle_user_id>/employments', EmploymentList.as_view(), name="employments"),
    path('<uuid:argyle_user_id>/profile', ProfileView.as_view(), name="profile")

]
