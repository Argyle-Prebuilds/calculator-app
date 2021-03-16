from rest_framework import serializers

from .models import ArgyleUser


class ArgyleUserSerializer(serializers.ModelSerializer):
    token_status = serializers.CharField(source='get_token_status', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ArgyleUser
        fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

