import datetime

from rest_auth import views
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.utils.argyle_api import ArgyleAPIWrapper
from api.utils.argyle_api_pagination import ArgyleApiPagination
from api.utils.exceptions import ArgyleException
from .models import ArgyleUser
from .serializers import ArgyleUserSerializer, ProfileSerializer, EmploymentSerializer, KeyMetricsSerializer
from .services.income_metrics.key_metrics import MetricsService
from .services.income_months.income_months_service import IncomeMonthService


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


class KeyMetricsList(generics.ListAPIView):
    """
    Return metrics for provided user grouped into 2 groups:
    - income_metrics - all metrics for last year, current year and projected, also grouped by companies
    - month_metrics - all gross pay values for last year, current year and projected, grouped by months
    - - - - - - - - - -
    Expected URL format: ((API_URL))/users/{:argyle_user_id}/key-metrics
    Expected payload:
    Method: GET
    Headers: {
            'Authorization': 'Token ((Admin Token))'
    }
    - - - - - - - - - -
    Example of returned data:
    Data: {
        "income_metrics": {
            "total_days": {
                "last_year_total": 366.0,
                "ytd_total": 34.0,
                "projected_total": 365.0,
                "companies": {
                    "amazon": {
                        "last_year_total": 366.0,
                        "ytd_total": 34.0,
                        "projected_total": 365.0
                    }
                }
            },

            "base_pay": {
                "last_year_total": 0.0,
                (...)
            },
            (...)
        },
        "month_metrics": {
            "1": {
                "1": 0.0,
                "2": 0.0,
                "3": 0.0,
                "4": 0.0,
                "5": 0.0,
                "6": 0.0,
                "7": 0.0,
                "8": 0.0,
                "9": 0.0,
                "10": 0.0,
                "11": 0.0,
                "12": 0.0
            },
            "2": {
                "1": 18560.17,
                "2": 0.0,
                "3": 0.0
            },
            "3": {
                "1": 6186.72,
                "2": 6186.72,
                "3": 6186.72,
                "4": 6186.72,
            }
        }
    }
    """

    serializer_class = KeyMetricsSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user_id = kwargs.get("argyle_user_id")
        now = datetime.datetime.now()

        current_year = now.year
        previous_year = current_year - 1

        argyle_wrapper = ArgyleAPIWrapper()

        employments = argyle_wrapper.get_all_employments(user_id)

        last_year_payouts = argyle_wrapper.get_all_payouts(user_id, from_start_date=datetime.date(previous_year, 1, 1),
                                                           to_start_date=datetime.date(previous_year, 12, 31))

        current_year_payouts = argyle_wrapper.get_all_payouts(user_id,
                                                              from_start_date=datetime.date(current_year, 1, 1),
                                                              to_start_date=datetime.date.today())

        metrics = MetricsService(last_year_payouts, current_year_payouts, employments)
        month_metrics = IncomeMonthService(last_year_payouts, current_year_payouts)

        response_data = {"income_metrics": metrics.get_metrics(),
                         "month_metrics": month_metrics.convert_to_chart_values(month_metrics.get_metrics())}

        return Response(response_data, status=views.status.HTTP_200_OK)


class EmploymentList(generics.ListAPIView):
    """
    Fetches all the employments of the provided user
    Expected URL format: ((API_URL))/users/{:argyle_user_id}/employments
    Expected payload:
    Method: GET
    Headers: {
            'Authorization': 'Token ((Admin Token))'
    }
    - - - - - - - - - -
    Example of returned data:
    Data: {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "a8447858-839d-4910-b9a0-492b5c9c90ad",
                "employer": "amazon",
                "job_title": "1635 - Helpline Agent",
                "job_type": "Salary",
                "hire_date": "2011-05-24T06:13:16Z",
                "termination_date": null,
                "termination_reason": null,
                "status": "active",
                "base_pay": 83.4
            }
        ]
    }
    """

    serializer_class = EmploymentSerializer

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get("argyle_user_id")
        offset = self.request.query_params.get("offset", 0)
        limit = self.request.query_params.get("limit", 10)
        argyle_wrapper = ArgyleAPIWrapper()

        employments = argyle_wrapper.get_employments(user_id, offset, limit)
        employments_list = EmploymentSerializer(employments['results'], many=True, context={"user_id": user_id}).data

        pagination = ArgyleApiPagination(int(employments['count']), int(limit), int(offset), request)
        response = pagination.get_paginated_response(employments_list)

        return Response(response, status=views.status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    """
    Retrieves user profile data.
    Expected URL format: ((API_URL))/users/{:argyle_user_id}/profile
    Expected payload:
    Method: GET
    Headers: {
            'Authorization': 'Token ((Admin Token))'
    }
    - - - - - - - - - -
    Example of returned data:
    Data: {
        "full_name": "Bob Jones",
        "birth_date": "1980-10-10",
        "email": "test1@argyle.io",
        "phone_number": "+18009000001",
        "employer": "amazon"
    }
    - - - - - - - - - -
    """

    serializer_class = ProfileSerializer

    def get_object(self):
        argyle_user_id = self.kwargs.get("argyle_user_id")
        argyle_wrapper = ArgyleAPIWrapper()
        profile_info = argyle_wrapper.fetch_argyle_profile(argyle_user_id)

        return profile_info
