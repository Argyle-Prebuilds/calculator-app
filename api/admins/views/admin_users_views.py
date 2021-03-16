from api.utils.exceptions import MailException
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from ..emails.admin_activation_email import send_activation_mail
from ..models import AdminUser
from ..serializers.admin_users_serializers import AdminUserSerializer, AdminUserListSerializer, \
    AdminUserActivateSerializer


class CreateAdminUser(generics.CreateAPIView):
    """
        Creates an instance of AdminUser with a randomly generated password, as well as
        sends an email to the user with a link redirecting to account activation.
        - - - - - - - - - -
        Expected payload:
        Method: POST
        Headers: {
            'Authorization': 'Token ((Admin Token))'
        }
        Data: {
            "email": "((String))",
        }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AdminUserSerializer

    def perform_create(self, serializer):
        admin_user = serializer.save()
        error = send_activation_mail(admin_user)
        # if sending activation email failed, the user is hard deleted from db
        if error:
            AdminUser.objects.get(id=admin_user.id).hard_delete()
            raise MailException(error)


class GetAdminUsers(generics.ListAPIView):
    """
        Retrieves a list of AdminUsers.
        - - - - - - - - - -
        Expected payload:
        Method: GET
        Headers: {
            'Authorization': 'Token ((Admin Token))'
        }
        - - - - - - - - - -
        Example of returned data:
        Data: [
            {
                "user_id": "1",
                "email": "jeff@a.com",
                "active": true
            },
            {
                "user_id": "2",
                "email": "john@a.com",
                "active": false
            }
        ]
    """
    queryset = AdminUser.objects.all().order_by('email')
    serializer_class = AdminUserListSerializer
    permission_classes = (IsAuthenticated,)


class DeleteAdminUser(generics.DestroyAPIView):
    """
        Soft-deletes the specified AdminUser.
        - - - - - - - - - -
        Expected URL format: ((API_URL))/users/delete/((userID))/
        Expected payload:
        Method: DELETE
        Headers: {
            'Authorization': 'Token ((Admin Token))'
        }
    """
    serializer_class = AdminUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AdminUser.objects.exclude(id=self.request.user.id)


class ActivateAdminUser(generics.UpdateAPIView):
    """
        Sets a new password to the AdminUser.user and flags the account as active.
        - - - - - - - - - -
        Expected payload:
        Method: PUT
        Data: {
            "password": "((password))",
            "password_confirmed": "((confirmed password))"
        }
    """
    permission_classes = (AllowAny,)
    serializer_class = AdminUserActivateSerializer
    queryset = AdminUser.objects.all()
