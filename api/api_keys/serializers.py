from rest_framework import serializers

from .models import ArgyleAPIKeys


class ArgyleAPIKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArgyleAPIKeys
        fields = '__all__'

    def create(self, validated_data):
        api_keys = ArgyleAPIKeys.objects.first()

        if api_keys:
            for key, value in validated_data.items():
                setattr(api_keys, key, value)
            api_keys.save()
            return api_keys

        api_keys = ArgyleAPIKeys.objects.create(**validated_data)
        return api_keys
