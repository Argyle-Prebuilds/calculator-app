import datetime
from decimal import Decimal
from django.test import TestCase
from admins.models import AdminUser
from users.services.income_metrics.date_service import DateService
from users.services.income_metrics.employment_service import EmploymentService
from users.services.income_metrics.income_metrics import IncomeMetrics
from users.services.income_metrics.key_metrics import MetricsService
from freezegun import freeze_time

from users.services.income_months.income_months import LAST_YEAR_TYPE, CURRENT_YEAR_TYPE, PROJECTED_TYPE, \
    PROJECTED_STDEV_TYPE, PROJECTED_STDEV_LOWER_TYPE, PROJECTED_STDEV_UPPER_TYPE, YTD_TYPE
from users.services.income_months.income_months_service import IncomeMonthService

payouts = [{
    "id": "a6b95412-e43a-4584-be9f-1dc101aa349a",
    "account": "f8bf3e18-09ba-428c-b197-6798f1b2b834",
    "document_id": "97f21592-b6b6-352a-91d7-e221bf0dd6e9",
    "employer": "walmart",
    "status": "completed",
    "type": "direct_deposit",
    "payout_date": "2020-04-22T00:00:00Z",
    "currency": "USD",
    "gross_pay": "1730.77",
    "deductions": "68.68",
    "taxes": "224.68",
    "net_pay": "1717.28",
    "bonuses": "0.00",
    "commission": "0.00",
    "overtime": "0.00",
    "reimbursements": "279.87",
    "hours": "80.00",
    "employer_address": {
        "line1": "4 Jackson St",
        "line2": "Apt C",
        "city": "Norton",
        "state": "MA",
        "postal_code": "27660",
        "country": "US"
    },
    "metadata": {
        "hours_breakdown": [{
            "hours": "80",
            "amount": "1730.77",
            "description": "Work Hours"
        }]
    }
}]

payouts2 = [{
    "id": "a6b95412-e43a-4584-be9f-1dc101aa349a",
    "account": "f8bf3e18-09ba-428c-b197-6798f1b2b834",
    "document_id": "97f21592-b6b6-352a-91d7-e221bf0dd6e9",
    "employer": "walmart",
    "status": "completed",
    "type": "direct_deposit",
    "payout_date": "2020-04-22T00:00:00Z",
    "currency": "USD",
    "gross_pay": "1730.77",
    "deductions": "68.68",
    "taxes": "224.68",
    "net_pay": "1717.28",
    "bonuses": "0.00",
    "commission": "0.00",
    "overtime": "0.00",
    "reimbursements": "279.87",
    "hours": "80.00",
    "employer_address": {
        "line1": "4 Jackson St",
        "line2": "Apt C",
        "city": "Norton",
        "state": "MA",
        "postal_code": "27660",
        "country": "US"
    },
    "metadata": {
        "hours_breakdown": [{
            "hours": "80",
            "amount": "1730.77",
            "description": "Work Hours"
        }]
    }
},
    {
        "id": "df8ggfd-e43a-4584-be9f-1dc101aa349a",
        "account": "f8bf3e18-09ba-428c-b197-6798f1b2b834",
        "document_id": "97f21592-b6b6-352a-91d7-534534g7dfg",
        "employer": "walmart",
        "status": "completed",
        "type": "direct_deposit",
        "payout_date": "2020-06-22T00:00:00Z",
        "currency": "USD",
        "gross_pay": "2100.77",
        "deductions": "68.68",
        "taxes": "312.33",
        "net_pay": "1827.28",
        "bonuses": "0.00",
        "commission": "0.00",
        "overtime": "0.00",
        "reimbursements": "279.87",
        "hours": "80.00",
        "employer_address": {
            "line1": "4 Jackson St",
            "line2": "Apt C",
            "city": "Norton",
            "state": "MA",
            "postal_code": "27660",
            "country": "US"
        },
        "metadata": {
            "hours_breakdown": [{
                "hours": "80",
                "amount": "1730.77",
                "description": "Work Hours"
            }]
        }
    },
    {
        "id": "df8ggfd-e43a-4584-be9f-1dc101aa349a",
        "account": "f8bf3e18-09ba-428c-b197-6798f1b2b834",
        "document_id": "97f21592-b6b6-352a-91d7-534534g7dfg",
        "employer": "amazon",
        "status": "completed",
        "type": "direct_deposit",
        "payout_date": "2020-06-22T00:00:00Z",
        "currency": "USD",
        "gross_pay": "2000.77",
        "deductions": "68.68",
        "taxes": "200.33",
        "net_pay": "1800.28",
        "bonuses": "0.00",
        "commission": "0.00",
        "overtime": "0.00",
        "reimbursements": "279.87",
        "hours": "80.00",
        "employer_address": {
            "line1": "4 Jackson St",
            "line2": "Apt C",
            "city": "Norton",
            "state": "MA",
            "postal_code": "27660",
            "country": "US"
        },
        "metadata": {
            "hours_breakdown": [{
                "hours": "80",
                "amount": "1730.77",
                "description": "Work Hours"
            }]
        }
    }
]

last_year_payouts = [{
    "id": "a6b95412-e43a-4584-be9f-1dc101aa349a",
    "account": "f8bf3e18-09ba-428c-b197-6798f1b2b834",
    "document_id": "97f21592-b6b6-352a-91d7-e221bf0dd6e9",
    "employer": "google",
    "status": "completed",
    "type": "direct_deposit",
    "payout_date": "2020-04-22T00:00:00Z",
    "currency": "USD",
    "gross_pay": "2000.77",
    "deductions": "68.68",
    "taxes": "224.68",
    "net_pay": "1800.28",
    "bonuses": "0.00",
    "commission": "0.00",
    "overtime": "0.00",
    "reimbursements": "279.87",
    "hours": "80.00",
    "employer_address": {
        "line1": "4 Jackson St",
        "line2": "Apt C",
        "city": "Norton",
        "state": "MA",
        "postal_code": "27660",
        "country": "US"
    },
    "metadata": {
        "hours_breakdown": [{
            "hours": "80",
            "amount": "1730.77",
            "description": "Work Hours"
        }]
    }},
    {
        "id": "df8ggfd-e43a-4584-be9f-1dc101aa349a",
        "account": "f8bf3e18-09ba-428c-b197-6798f1b2b834",
        "document_id": "97f21592-b6b6-352a-91d7-534534g7dfg",
        "employer": "amazon",
        "status": "completed",
        "type": "direct_deposit",
        "payout_date": "2020-06-22T00:00:00Z",
        "currency": "USD",
        "gross_pay": "1000",
        "deductions": "68.68",
        "taxes": "200.33",
        "net_pay": "500",
        "bonuses": "0.00",
        "commission": "0.00",
        "overtime": "0.00",
        "reimbursements": "279.87",
        "hours": "80.00",
        "employer_address": {
            "line1": "4 Jackson St",
            "line2": "Apt C",
            "city": "Norton",
            "state": "MA",
            "postal_code": "27660",
            "country": "US"
        },
        "metadata": {
            "hours_breakdown": [{
                "hours": "80",
                "amount": "1730.77",
                "description": "Work Hours"
            }]
        }

    }]


class MetricsTest(TestCase):

    def setUp(self) -> None:
        self.admin = AdminUser.objects.create()

    def test_empty_payouts_key_metrics(self):
        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=[],
                                             current_year_payouts=[], employments=[])

            metrics = metrics_service.get_metrics()

        self.assertEqual(metrics['gross_pay'], {
            'last_year_total': Decimal('0'),
            'ytd_total': Decimal('0'),
            'projected_total': Decimal('0'),
            'companies': []
        })

    def test_company_key_metrics(self):
        employments = (
            {
                "employer": "amazon",
                "hire_datetime": "2020-11-01T17:29:08.724441Z",
                "termination_datetime": None,
            },
        )

        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=last_year_payouts,
                                             current_year_payouts=payouts2, employments=employments)

            metrics = metrics_service.get_metrics()

        self.assertEqual(metrics['gross_pay'], {
            'last_year_total': Decimal('3000.77'),
            'ytd_total': Decimal('5832.31'),
            'projected_total': Decimal('24009.24'),  # only using active employers- amazon
            'companies': {
                'google': {'last_year_total': Decimal('2000.77'), 'ytd_total': Decimal('0'),
                           'projected_total': Decimal('0')},
                'amazon': {'last_year_total': Decimal('1000'), 'ytd_total': Decimal('2000.77'),
                           'projected_total': Decimal('24009.24')},
                'walmart': {'last_year_total': Decimal('0'), 'ytd_total': Decimal('3831.54'),
                            'projected_total': Decimal('0')},
            }
        })

    def test_pay_frequency_weekly(self):
        test_last_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2020-06-01T00:00:00Z",
                "hours": "40.00",
            },
            {
                "employer": "amazon",
                "payout_date": "2020-06-08T00:00:00Z",
                "hours": "40.00",
            },
            {
                "employer": "amazon",
                "payout_date": "2020-06-15T00:00:00Z",
                "hours": "40.00",
            },
        ]

        current_year_payouts = [{
            "employer": "amazon",
            "payout_date": "2021-01-01T00:00:00Z",
            "hours": "40.00",
        },
            {
                "employer": "amazon",
                "payout_date": "2021-02-01T00:00:00Z",
                "hours": "40.00",
            }]

        with freeze_time("2021-02-02"):
            metrics_service = MetricsService(last_year_payouts=test_last_year_payouts,
                                             current_year_payouts=current_year_payouts, employments=[])

            metrics = metrics_service.get_metrics()
            self.assertEqual(metrics['pay_frequency'], {
                'last_year_total': {IncomeMetrics.WEEKLY},
                'ytd_total': {IncomeMetrics.MONTHLY},
                'projected_total': set(),
                'companies': {
                    'amazon': {'last_year_total': {IncomeMetrics.WEEKLY}, 'ytd_total': {IncomeMetrics.MONTHLY},
                               'projected_total': set()}
                }})

    def test_pay_frequency_monthly(self):
        test_last_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2020-07-08T00:00:00Z",
                "hours": "40.00",
            },
            {
                "employer": "amazon",
                "payout_date": "2020-06-01T00:00:00Z",
                "hours": "40.00",
            },

            {
                "employer": "amazon",
                "payout_date": "2020-08-03T00:00:00Z",
                "hours": "40.00",
            }
        ]

        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=test_last_year_payouts,
                                             current_year_payouts=[], employments=[])

            metrics = metrics_service.get_metrics()
            self.assertEqual(metrics['pay_frequency'], {
                'last_year_total': {IncomeMetrics.MONTHLY},
                'ytd_total': set(),
                'projected_total': set(),
                'companies': {
                    'amazon': {'last_year_total': {IncomeMetrics.MONTHLY}, 'ytd_total': set(),
                               'projected_total': set()}}
            })

    def test_gross_monthly_with_last_year(self):
        test_last_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2020-06-01T00:00:00Z",
                "gross_pay": 2000,
                "hours": 20
            },
            {
                "employer": "amazon",
                "payout_date": "2020-07-08T00:00:00Z",
                "gross_pay": 2000,
                "hours": 30
            },
            {
                "employer": "amazon",
                "payout_date": "2020-08-03T00:00:00Z",
                "gross_pay": 2000,
                "hours": 20
            },
        ]

        current_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2021-06-01T00:00:00Z",
                "gross_pay": 4000,
                "hours": 20
            },
        ]

        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=test_last_year_payouts,
                                             current_year_payouts=current_year_payouts, employments=[])

            metrics = metrics_service.get_metrics()

            self.assertEqual(metrics['gross_monthly_with_last_year'], {
                'last_year_total': Decimal('500'),
                'ytd_total': Decimal('769.23'),
                'projected_total': Decimal('0'),
                'companies': {
                    'amazon': {'last_year_total': Decimal('500'), 'ytd_total': Decimal('769.23'),
                               'projected_total': Decimal('0')},
                }
            })

    def test_total_days(self):
        test_last_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2020-06-01T00:00:00Z",
                "gross_pay": 2000,
                "hours": 20
            },
            {
                "employer": "amazon",
                "payout_date": "2020-07-08T00:00:00Z",
                "gross_pay": 2000,
                "hours": 30
            },
            {
                "employer": "amazon",
                "payout_date": "2020-08-03T00:00:00Z",
                "gross_pay": 2000,
                "hours": 20
            },
        ]

        current_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2021-06-01T00:00:00Z",
                "gross_pay": 4000,
                "hours": 20
            },
        ]

        employments = (
            {
                "employer": "amazon",
                "hire_datetime": "2020-11-01T17:29:08.724441Z",
                "termination_datetime": None,
            },
            {
                "employer": "google",
                "hire_datetime": "2021-01-20T17:29:08.724441Z",
                "termination_datetime": None,
            },
        )

        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=test_last_year_payouts,
                                             current_year_payouts=current_year_payouts, employments=employments)

            metrics = metrics_service.get_metrics()

            self.assertEqual(metrics['total_days'], {
                'last_year_total': Decimal('61'),
                'ytd_total': Decimal('28'),
                'projected_total': Decimal('365'),
                'companies': {
                    'amazon': {'last_year_total': Decimal('61'), 'ytd_total': Decimal('28'),
                               'projected_total': Decimal('365')},
                    'google': {'last_year_total': Decimal('0'), 'ytd_total': Decimal('9'),
                               'projected_total': Decimal('346')},
                }
            })

    def test_pay_frequency_weekly_monthly(self):
        test_last_year_payouts = [
            {
                "employer": "amazon",
                "payout_date": "2020-06-01T00:00:00Z",
                "hours": 40
            },
            {
                "employer": "amazon",
                "payout_date": "2020-07-08T00:00:00Z",
                "hours": 50
            },
            {
                "employer": "amazon",
                "payout_date": "2020-08-03T00:00:00Z",
                "hours": 40
            },
            {
                "employer": "google",
                "payout_date": "2020-07-08T00:00:00Z",
                "hours": 50
            },
            {
                "employer": "google",
                "payout_date": "2020-07-15T00:00:00Z",
                "hours": 40
            }
        ]

        current_year_payouts = [{
            "employer": "amazon",
            "payout_date": "2021-01-01T00:00:00Z",
            "hours": "40.00",
        },
            {
                "employer": "amazon",
                "payout_date": "2021-02-01T00:00:00Z",
                "hours": "40.00",
            }]
        employments = (
            {
                "employer": "amazon",
                "hire_datetime": "2020-11-01T17:29:08.724441Z",
                "termination_datetime": None,
            },
        )

        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=test_last_year_payouts,
                                             current_year_payouts=current_year_payouts, employments=employments)

            metrics = metrics_service.get_metrics()

            self.assertEqual(metrics['pay_frequency'], {
                'last_year_total': {IncomeMetrics.MONTHLY, IncomeMetrics.WEEKLY},
                'ytd_total': {IncomeMetrics.MONTHLY},
                'projected_total': {IncomeMetrics.MONTHLY},
                'companies': {
                    'amazon': {'last_year_total': {IncomeMetrics.MONTHLY}, 'ytd_total': {IncomeMetrics.MONTHLY},
                               'projected_total': {IncomeMetrics.MONTHLY}},
                    'google': {'last_year_total': {IncomeMetrics.WEEKLY}, 'ytd_total': set(),
                               'projected_total': set()}
                }

            })


class DateMetrics(TestCase):
    def test_calculate_days_in_year(self):
        params = (
            ((datetime.date(2019, 1, 1), datetime.date(2019, 12, 31), 2019), 365),
            ((datetime.date(2019, 1, 1), datetime.date(2019, 1, 31), 2019), 31),
            ((datetime.date(2019, 1, 1), datetime.date(2020, 1, 31), 2019), 365),
            ((datetime.date(2019, 1, 1), datetime.date(2020, 1, 31), 2020), 31),
            ((datetime.date(2019, 1, 1), None, 2020), 366),
            ((datetime.date(2019, 1, 1), None, 2021), 28),  # freeze time 2021-01-28
            ((datetime.date(2021, 1, 1), datetime.date(2021, 1, 10), 2021), 10),  # freeze time 2021-01-28
        )

        for input_values, expected in params:
            from_date, to_date, year = input_values

            with freeze_time("2021-01-28"):
                days = DateService.calculate_work_days_in_year(from_date, to_date, year)

            self.assertEqual(days, expected)

    def test_calculate_projected_days(self):
        params = (
            ((datetime.date(2019, 1, 1), datetime.date(2019, 12, 31), 2019), 365),
            ((datetime.date(2019, 1, 1), datetime.date(2019, 1, 31), 2019), 31),
            ((datetime.date(2019, 1, 1), datetime.date(2020, 1, 31), 2019), 365),
            ((datetime.date(2019, 1, 1), datetime.date(2020, 1, 31), 2020), 31),
            ((datetime.date(2019, 1, 1), None, 2020), 366),
            ((datetime.date(2019, 1, 5), None, 2021), 365),  # freeze time 2021-01-28
            ((datetime.date(2021, 1, 5), None, 2021), 361),  # freeze time 2021-01-28
            ((datetime.date(2021, 1, 1), datetime.date(2021, 1, 10), 2021), 10),  # freeze time 2021-01-28
            ((datetime.date(2020, 11, 1), None, 2021), 365),  # freeze time 2021-01-28
        )

        for input_values, expected in params:
            from_date, to_date, year = input_values

            with freeze_time("2021-01-28"):
                days = DateService.calculate_projected_days_in_year(from_date, to_date, year)

            self.assertEqual(days, expected)

    def test_total_days_in_key_metrics(self):
        employments = (
            {
                "employer": "google",
                "hire_datetime": "2019-01-01T17:29:08.724441Z",
                "termination_datetime": "2020-12-31T17:29:08.724441Z",
            },
            {
                "employer": "amazon",
                "hire_datetime": "2020-11-01T17:29:08.724441Z",
                "termination_datetime": None,
            },
            {
                "employer": "walmart",
                "hire_datetime": "2021-01-01T17:29:08.724441Z",
                "termination_datetime": "2021-01-10T17:29:08.724441Z",
            },
        )
        with freeze_time("2021-01-28"):
            metrics_service = MetricsService(last_year_payouts=last_year_payouts,
                                             current_year_payouts=payouts2, employments=employments)

            metrics = metrics_service.get_metrics()

        self.assertEqual(metrics['total_days']['companies'], {
            'google': {'last_year_total': Decimal(366), 'ytd_total': Decimal(0), 'projected_total': Decimal(0)},
            'walmart': {'last_year_total': Decimal(0), 'ytd_total': Decimal(10), 'projected_total': Decimal(10)},
            'amazon': {'last_year_total': Decimal(61), 'ytd_total': Decimal(28), 'projected_total': Decimal(365)}
        })

    def test_get_employments_by_date(self):
        employments = (
            {
                "employer": "amazon",
                "hire_datetime": "2019-10-27T17:29:08.724441Z",
                "termination_datetime": "2020-11-27T17:29:08.724441Z",
            },
            {
                "employer": "test",
                "hire_datetime": "2020-02-27T17:29:08.724441Z",
                "termination_datetime": "2020-11-27T17:29:08.724441Z",
            },
            {
                "employer": "google",
                "hire_datetime": "2021-01-01T17:29:08.724441Z",
                "termination_datetime": None,
            },
            {
                "employer": "kroger",
                "hire_datetime": "2019-01-01T17:29:08.724441Z",
                "termination_datetime": "2021-01-08T17:29:08.724441Z",
            }
        )
        with freeze_time("2021-01-28"):
            last_year_employments = EmploymentService.get_employment_from_last_year(employments)
            last_year_employers = [employment['employer'] for employment in last_year_employments]

        self.assertTrue(employments[0]['employer'] in last_year_employers)
        self.assertTrue(employments[1]['employer'] in last_year_employers)
        self.assertFalse(employments[2]['employer'] in last_year_employers)
        self.assertTrue(employments[3]['employer'] in last_year_employers)

        with freeze_time("2021-01-28"):
            current_year_employments = EmploymentService.get_employment_from_current_year(employments)
            current_year_employers = [employment['employer'] for employment in current_year_employments]

        self.assertFalse(employments[0]['employer'] in current_year_employers)
        self.assertFalse(employments[1]['employer'] in current_year_employers)
        self.assertTrue(employments[2]['employer'] in current_year_employers)
        self.assertTrue(employments[3]['employer'] in current_year_employers)


class TestIncomeMonths(TestCase):
    JANUARY = 1
    FEBRUARY = 2
    APRIL = 4
    MAY = 5

    def test_income_months(self):
        test_last_year_payouts = [
            {
                "payout_date": "2020-04-11T00:00:00Z",
                "gross_pay": "2000.00",
            },
            {
                "payout_date": "2020-04-22T00:00:00Z",
                "gross_pay": "2300.00",
            }, {
                "payout_date": "2020-05-22T00:00:00Z",
                "gross_pay": "2000.00",
            }, {
                "payout_date": "2020-06-22T00:00:00Z",
                "gross_pay": "2000.00",
            },

        ]
        test_current_payouts = [{
            "payout_date": "2021-01-22T00:00:00Z",
            "gross_pay": "2600.00",
        }]

        with freeze_time("2021-02-02"):
            metrics_service = IncomeMonthService(last_year_payouts=test_last_year_payouts,
                                                 current_year_payouts=test_current_payouts)

            metrics = metrics_service.get_metrics()

            self.assertEqual(metrics[LAST_YEAR_TYPE][self.JANUARY], Decimal(0))
            self.assertEqual(metrics[LAST_YEAR_TYPE][self.APRIL], Decimal(4300))
            self.assertEqual(metrics[LAST_YEAR_TYPE][self.MAY], Decimal(2000))
            self.assertEqual(metrics[CURRENT_YEAR_TYPE][self.JANUARY], Decimal(2600))
            self.assertEqual(metrics[PROJECTED_TYPE][self.JANUARY], Decimal(2600))
            self.assertEqual(metrics[PROJECTED_TYPE][self.FEBRUARY], Decimal(1300))

    def test_income_months_with_stdev(self):
        test_last_year_payouts = [
            {"payout_date": "2020-01-01T00:00:00Z", "gross_pay": "2000.00"},
            {"payout_date": "2020-02-01T00:00:00Z", "gross_pay": "2500.00"},
            {"payout_date": "2020-03-01T00:00:00Z", "gross_pay": "3100.00"},
            {"payout_date": "2020-04-01T00:00:00Z", "gross_pay": "2400.00"},
            {"payout_date": "2020-05-01T00:00:00Z", "gross_pay": "2300.00"},
            {"payout_date": "2020-06-01T00:00:00Z", "gross_pay": "2250.00"},
            {"payout_date": "2020-07-01T00:00:00Z", "gross_pay": "1980.00"},
            {"payout_date": "2020-08-01T00:00:00Z", "gross_pay": "2000.00"},
            {"payout_date": "2020-09-01T00:00:00Z", "gross_pay": "2400.00"},
            {"payout_date": "2020-10-01T00:00:00Z", "gross_pay": "2550.00"},
            {"payout_date": "2020-11-01T00:00:00Z", "gross_pay": "2700.00"},
            {"payout_date": "2020-12-01T00:00:00Z", "gross_pay": "3600.00"},
        ]
        test_current_payouts = [
            {"payout_date": "2021-01-01T00:00:00Z", "gross_pay": "3890.00"},
            {"payout_date": "2021-02-01T00:00:00Z", "gross_pay": "4010.00"},
        ]

        with freeze_time("2021-02-28"):
            metrics_service = IncomeMonthService(last_year_payouts=test_last_year_payouts,
                                                 current_year_payouts=test_current_payouts)

        metrics = metrics_service.get_metrics()

        self.assertEqual(metrics[LAST_YEAR_TYPE][self.JANUARY], Decimal('2000'))
        self.assertEqual(metrics[LAST_YEAR_TYPE][self.FEBRUARY], Decimal('2500'))
        self.assertEqual(metrics[CURRENT_YEAR_TYPE][self.JANUARY], Decimal('3890'))
        self.assertEqual(metrics[CURRENT_YEAR_TYPE][self.FEBRUARY], Decimal('4010'))
        self.assertEqual(metrics[PROJECTED_TYPE][self.JANUARY], Decimal('3890'))
        self.assertEqual(metrics[PROJECTED_TYPE][self.FEBRUARY], Decimal('4010'))

        self.assertEqual(metrics[PROJECTED_STDEV_TYPE][self.JANUARY], Decimal('600.85'))
        self.assertEqual(metrics[PROJECTED_STDEV_TYPE][self.FEBRUARY], Decimal('690.85'))
        self.assertEqual(metrics[PROJECTED_STDEV_UPPER_TYPE][self.JANUARY], Decimal('4490.85'))
        self.assertEqual(metrics[PROJECTED_STDEV_LOWER_TYPE][self.JANUARY], Decimal('3289.15'))
