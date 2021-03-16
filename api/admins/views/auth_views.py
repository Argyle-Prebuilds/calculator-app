from admins.emails.password_reset_email import send_password_reset_mail
from admins.models import AdminUser
from admins.serializers.auth_serializers import AdminUserAuthSerializer, TokenSerializer, \
    AdminUserPasswordUpdateSerializer, \
    PasswordResetSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response


class LoginView(APIView):
    """
    View for logging admin user into app. Returns token if the provided credentials are valid.
    - - - - - - - - - -
    Expected URL format: ((API_URL))/auth/login
    Expected payload:
    Method: POST
    Data: {
        "email": "((String))",
        "password": "((String))",
    }
    - - - - - - - - - -
    Example of returned data:
    Data: {
        "token": "08864d4e0b893e6f1ffde57aa4d4c2959aa1423d",
        "user": "72a4e0c3-f93c-4999-89ba-b4987e1e7623"
    }
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        auth_serializer = AdminUserAuthSerializer(data=data)
        auth_serializer.is_valid()

        if auth_serializer.errors:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=auth_serializer.errors)

        admin_user = AdminUser.objects.get(email=auth_serializer.data['email'])

        token_serializer = TokenSerializer(data={
            'admin_user': admin_user.id
        })

        token_serializer.is_valid()

        if token_serializer.errors:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=token_serializer.errors)

        token = token_serializer.save()

        return Response(status=status.HTTP_200_OK, data={
            'token': token.key,
            'user': admin_user.id
        })


class PasswordResetSendMailView(APIView):
    """
    View for resetting admin user password. If the provided email exists the app sends an email containing a link redirecting
    to the password-reset page.
    - - - - - - - - - -
    Expected URL format: ((API_URL))/auth/password-reset
    Expected payload:
    Method: POST
    Data: {
        "email": "((String))",
    }
    - - - - - - - - - -
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        serializer = PasswordResetSerializer(data=data)
        serializer.is_valid()

        if serializer.errors:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        admin_user = AdminUser.objects.get(email=data['email'])
        admin_user.password_awaiting_reset = True
        admin_user.save()

        error = send_password_reset_mail(admin_user=admin_user)
        if error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'email': error
            })
        return Response(status=status.HTTP_200_OK)


class PasswordUpdateView(APIView):
    """
    Updating password. Makes sure that the user is flagged for password reset and sets
    the new password.
    - - - - - - - - - -
    Expected payload:
    Method: POST
    Data: {
        "id": "((adminUserID))",
        "password": "((String))",
        "password_confirmed": "((String))"
    }
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data

        serializer = AdminUserPasswordUpdateSerializer(data=data)
        serializer.is_valid()

        if serializer.errors:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        serializer.update()

        return Response(status=status.HTTP_200_OK)


class ValidateTokenView(APIView):
    """
    Checking whether the provided token is valid.
    - - - - - - - - - -
    Expected payload:
    Method: POST
    Data: {
        "token": "((Token))",
    }
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        if 'token' not in data or not Token.objects.filter(key=data['token']).first():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_200_OK)
