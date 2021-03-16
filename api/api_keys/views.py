from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ArgyleAPIKeys
from .serializers import ArgyleAPIKeysSerializer


class APIKeyListCreateView(generics.ListCreateAPIView):
    """
        Creates or retrieves the ArgyleAPIKeys instance data.
        - - - - - - - - - -
        Expected payload:
        Method: GET
        Headers: {
            'Authorization': 'Token ((Admin Token))'
        }
        - - - - - - - - - -
        Example of returned data:
        Data: {
            "id": 1,
            "client_id": "((client_id))",
            "client_secret": "((client_secret))",
            "plugin_key": "((plugin_key))"
        }
        - - - - - - - - - -

        - - - - - - - - - -
        Expected payload:
        Method: POST
        Headers: {
            'Authorization': 'Token ((Admin Token))'
        }
        Data: {
            "client_id": "((client_id))",
            "client_secret": "((client_secret))",
            "plugin_key": "((plugin_key))"
            "is_sandbox_mode": "((Bool))"
        }
        - - - - - - - - - -
        Example of returned data:
        Data: {
            "id": 1,
            "client_id": "((client_id))",
            "client_secret": "((client_secret))",
            "plugin_key": "((plugin_key))"
            "is_sandbox_mode": "((Bool))"
        }
    """
    serializer_class = ArgyleAPIKeysSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ArgyleAPIKeys.get_argyle_keys()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()

        data = {
            'client_id': '',
            'client_secret': '',
            'plugin_key': ''
        }

        if self.get_queryset():
            data = serializer(self.get_queryset(), context={'request': self.request}).data

        return Response(data=data, status=status.HTTP_200_OK)
