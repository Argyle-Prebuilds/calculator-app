from decimal import Decimal

from rest_framework import serializers

from api.utils.argyle_api import ArgyleAPIWrapper
from api.utils.dates import get_date_from_str
from .models import ArgyleUser


class ArgyleUserSerializer(serializers.ModelSerializer):
    token_status = serializers.CharField(source='get_token_status', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ArgyleUser
        fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class KeyMetricsSerializer(serializers.Serializer):
    token_status = serializers.CharField(source='get_token_status', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('first_name', 'last_name', 'email')


class EmploymentSerializer(serializers.Serializer):
    id = serializers.CharField()
    employer = serializers.CharField()
    job_title = serializers.CharField()
    job_type = serializers.CharField(source='type')
    hire_date = serializers.DateTimeField(source='hire_datetime')
    termination_date = serializers.DateTimeField(source='termination_datetime')
    termination_reason = serializers.CharField()
    status = serializers.CharField()
    base_pay = serializers.SerializerMethodField()

    def get_base_pay(self, obj):
        argyle_wrapper = ArgyleAPIWrapper()
        user_id = self.context.get('user_id')
        termination_date = get_date_from_str(obj['termination_datetime']) if obj['termination_datetime'] else None
        payouts = argyle_wrapper.get_all_payouts_by_company_and_date(user_id=user_id, from_start_date=get_date_from_str(
            obj['hire_datetime']), to_start_date=termination_date, employer=obj['employer'])

        gross_pay_sum = Decimal(0)
        hours_sum = Decimal(0)

        for payout in payouts:
            gross_pay_sum += Decimal(payout['gross_pay'])
            hours_sum += Decimal(payout['hours'])

        if hours_sum == 0:
            return 0

        avg_rate = round(gross_pay_sum / hours_sum, 2)

        return avg_rate


class ProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    birth_date = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    employer = serializers.CharField()
