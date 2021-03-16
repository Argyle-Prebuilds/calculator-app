from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password as auth_validate_password

from admins.models import AdminUser


class AdminUserPasswordUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    password = serializers.CharField(required=True)
    password_confirmed = serializers.CharField(required=True)

    class Meta:
        model = AdminUser
        fields = ['password', 'password_confirmed', 'id']

    def validate_password(self, value):
        """
            Validate that passwords match
        """
        if self.initial_data['password_confirmed'] != value:
            raise serializers.ValidationError('Passwords do not match')
        auth_validate_password(self.initial_data['password_confirmed'])
        return value

    def validate_password_confirmed(self, value):
        """
            Validate that passwords match
        """
        if self.initial_data['password'] != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_id(self, value):
        """
            Validate whether the user exists and is awaiting password reset
        """
        try:
            admin_user = AdminUser.objects.get(id=value)
            if not admin_user.password_awaiting_reset:
                raise serializers.ValidationError(
                    'User is not awaiting password reset.')
        except AdminUser.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')

        return value

    def update(self):
        """
            Updates the user's password and flag as not awaiting password reset anymore
        """
        admin_user = AdminUser.objects.get(id=self.validated_data['id'])
        admin_user.set_password(self.validated_data['password'])
        admin_user.password_awaiting_reset = False
        admin_user.save()


class AdminUserAuthSerializer(serializers.Serializer):
    """
        AdminUser authentication validator
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = AdminUser
        fields = ('email', 'password')

    def validate_email(self, value):
        """
            Validate whether the user exists
        """
        try:
            AdminUser.objects.get(email=value)
        except AdminUser.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')

        return value

    def validate_password(self, value):
        """
            Validate whether the password matches
        """

        try:
            admin_user = AdminUser.objects.get(email=self.initial_data['email'])
            if not admin_user.check_password(value):
                raise serializers.ValidationError('Invalid password.')
        except AdminUser.DoesNotExist:
            pass

        return value


class PasswordResetSerializer(serializers.Serializer):
    """
         Email validation for Password Reset
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            AdminUser.objects.get(email=value)
        except AdminUser.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')

        return value


class TokenSerializer(serializers.Serializer):
    """
        Creates a Token and removes the previous one if it existed
    """
    admin_user = serializers.UUIDField(required=True)

    def validate_admin_user(self, value):
        try:
            AdminUser.objects.get(id=value)
        except AdminUser.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return value

    def save(self):
        admin_user = AdminUser.objects.get(id=self.validated_data['admin_user'])
        existing_token = Token.objects.filter(user=admin_user)

        if existing_token:
            existing_token.delete()

        new_token = Token.objects.create(user=admin_user)
        return new_token
