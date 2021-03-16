from api.utils.exceptions import ArgyleException
from api.utils.argyle_api import ArgyleAPIWrapper
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ArgyleUser
from .serializers import ArgyleUserSerializer


class ArgyleUsersListCreate(generics.ListCreateAPIView):
    """
    Fetch all users list or creates a new user.
    - - - - - - - - - -
    Expected URL format: ((API_URL))/users/
    Expected payload:
    Method: GET
    Headers: {
            'Authorization': 'Token ((Admin Token))'
    }
    - - - - - - - - - -
    Example of returned data:
    Data : {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "token_status": "active",
                "full_name": "Bob Jones",
                "argyle_id": "5e1e41df-f16f-4613-bca0-70713ffec802",
                "token_expiry": 1614944456,
                "email": "test1@argyle.io",
                "first_name": "Bob",
                "last_name": "Jones"
            }
        ]
    }
    - - - - - - - - - -
    - - - - - - - - - -
    Expected payload:
    Method: POST
    Data: {
        "argyle_id": "((UUID String))",
        "token_expiry": "((Timestamp String))",
    }
    - - - - - - - - - -
    Example of returned data:
    Data: {
        "data": {
        "id": 3,
        "token_status": "active",
        "full_name": "Sarah Longfield",
        "argyle_id": "b0252647-0cb0-4344-adf8-89596af74e0a",
        "token_expiry": 1613924091,
        "email": "test2@argyle.io",
        "first_name": "Sarah",
        "last_name": "Longfield"
        },
        "message": "New user has been created."
    }
    """

    serializer_class = ArgyleUserSerializer
    queryset = ArgyleUser.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = data['argyle_id']
        token_expiry = data['token_expiry']
        argyle_profile = ArgyleAPIWrapper().fetch_argyle_profile(user_id)

        if not argyle_profile:
            raise ArgyleException('No user connected with provided token has been found.')

        # if the user already exists, we override the current token_expiry
        try:
            argyle_user = ArgyleUser.objects.get(argyle_id=argyle_profile['id'])
            data = {'token_expiry': token_expiry}
            serializer = self.serializer_class(argyle_user, data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'data': serializer.data,
                             'message': 'The user with provided token has been found. Token expiry date has been updated.'})

        # otherwise, new user is created
        except ArgyleUser.DoesNotExist:
            argyle_user_data = {
                'argyle_id': user_id,
                'first_name': argyle_profile['first_name'],
                'last_name': argyle_profile['last_name'],
                'email': argyle_profile['email'],
                'token_expiry': token_expiry
            }
            serializer = self.serializer_class(data=argyle_user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'data': serializer.data,
                             'message': 'New user has been created.'})


class ArgyleUsersDelete(generics.DestroyAPIView):
    """
    Deletes used with provided id.
    - - - - - - - - - -
    Expected URL format: ((API_URL))/users/{:argyle_user_id}
    Expected payload:
    Method: DELETE
    Headers: {
            'Authorization': 'Token ((Admin Token))'
    }
    - - - - - - - - - -
    """
    serializer_class = ArgyleUserSerializer
    queryset = ArgyleUser.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'argyle_id'
    lookup_url_kwarg = 'argyle_user_id'

