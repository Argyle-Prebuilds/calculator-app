from django.contrib.auth.password_validation import validate_password as auth_validate_password
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import AdminUser


class AdminUserListSerializer(serializers.ModelSerializer):
    """
        Serializer for list of Admin Users
    """

    class Meta:
        model = AdminUser
        fields = ['id', 'email', 'is_active']


class AdminUserActivateSerializer(serializers.ModelSerializer):
    """
        AdminUser activator and password setup
    """
    password = serializers.CharField(required=True, write_only=True)
    password_confirmed = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = AdminUser
        fields = ['password', 'password_confirmed']

    def validate_password(self, value):
        """
            Validate that passwords match
        """
        if 'password_confirmed' in self.initial_data:
            if self.initial_data['password_confirmed'] != value:
                raise serializers.ValidationError('Passwords do not match')
            auth_validate_password(self.initial_data['password_confirmed'])
        return value

    def validate_password_confirmed(self, value):
        """
            Validate that passwords match
        """
        if 'password' in self.initial_data:
            if self.initial_data['password'] != value:
                raise serializers.ValidationError('Passwords do not match')
        return value

    def validate(self, value):
        """
            Test whether the user has not been already activated
        """
        if self.instance.is_active:
            raise serializers.ValidationError(
                {'active': 'User has already been activated'})
        return value

    def update(self, instance, validated_data):
        """
            Update passwords and set user as active
        """
        instance.set_password(validated_data['password'])
        instance.is_active = True
        instance.save()
        return instance


class AdminUserPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password_confirmed = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = AdminUser
        fields = ['password', 'password_confirmed']

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

    def update(self, instance, validated_data):
        """
            Updates the user's password and flag as not awaiting password reset anymore
        """
        instance.set_password(validated_data['password'])
        instance.password_awaiting_reset = False
        instance.save()
        return instance


class AdminUserEmailSerializer(serializers.Serializer):
    """
        AdminUser email validator
    """
    email = serializers.EmailField(required=True)

    def update(self, instance, validated_data):
        instance.password_awaiting_reset = True
        instance.save()
        return instance


class AdminUserSerializer(serializers.ModelSerializer):
    """
        Serializes the AdminUser model
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = AdminUser
        fields = ['email']

    def validate_email(self, value):
        if AdminUser.objects.filter(email=value).exists():
            raise ValidationError('Account with provided email already exists')
        return value

    def create(self, validated_data):
        """
            Creating user and generating a random password
        """
        instance = AdminUser.objects.create_user(**validated_data)
        instance.set_password(get_random_string(length=20))
        instance.save()
        return instance
