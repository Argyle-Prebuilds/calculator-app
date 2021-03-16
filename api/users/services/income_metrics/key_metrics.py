from decimal import Decimal
from typing import Tuple

from api.utils.dates import get_date_from_str
from users.services.income_metrics.employment_service import get_current_year, EmploymentService
from users.services.income_metrics.income_metrics import CurrentYearIncomeMetrics, \
    LastYearIncomeMetrics, ProjectedIncomeMetrics

# All keys needed to be in response with default value
ALL_KEYS = (
    ('total_days', Decimal(0)),
    ('hours', Decimal(0)),
    ('hours_per_week', Decimal(0)),
    ('pay_frequency', set()),
    ('rate_of_pay', Decimal(0)),
    ('base_pay', Decimal(0)),
    ('overtime', Decimal(0)),
    ('commission', Decimal(0)),
    ('bonuses', Decimal(0)),
    ('reimbursements', Decimal(0)),
    ('gross_pay', Decimal(0)),
    ('deductions', Decimal(0)),
    ('net_pay', Decimal(0)),
    ('taxes', Decimal(0)),
    ('gross_monthly', Decimal(0)),
    ('gross_monthly_with_last_year', Decimal(0)))


class YearMetricsService:
    """
        Year Metrics Service is a helper service, that keep metrics by company, update them by employment and payouts data
    """

    def __init__(self, payouts, employments, year, last_year_metrics=None):
        self.metrics = {}

        self.last_year_metrics = last_year_metrics
        self.update_from_payouts(payouts, year)
        self.update_from_employments(employments, year)

    def update_from_employments(self, employments, year):

        for employment in employments:
            employer = employment['employer']
            hire_date = get_date_from_str(employment['hire_datetime'])
            termination_date = get_date_from_str(employment['termination_datetime']) if employment[
                'termination_datetime'] else None

            if employer not in self.metrics:
                self.metrics[employer] = CurrentYearIncomeMetrics(
                    year) if year == get_current_year() else LastYearIncomeMetrics(year)

            self.metrics[employer].hire_date = hire_date
            self.metrics[employer].termination_date = termination_date

    def update_from_payouts(self, payouts: list, year):
        for payout in payouts:
            employer = payout['employer']

            if employer not in self.metrics:
                self.metrics[employer] = CurrentYearIncomeMetrics(
                    year) if year == get_current_year() else LastYearIncomeMetrics(year)

            self.metrics[employer].add_payout(payout)
            if self.last_year_metrics and employer in self.last_year_metrics.keys():
                self.metrics[employer].set_last_year_metrics(self.last_year_metrics[employer])

    def get_metrics_by_company(self):
        return self.metrics


class MetricsService:
    """
        Metrics Service - responsible for prepare all income metrics for last year, current year and projected,
         also grouped by companies
    """

    def __init__(self, last_year_payouts, current_year_payouts, employments):
        self.active_employers = EmploymentService.get_active_employers(employments)
        self.last_year_metrics = YearMetricsService(last_year_payouts,
                                                    EmploymentService.get_employment_from_last_year(employments),
                                                    get_current_year() - 1).get_metrics_by_company()
        self.current_year_metrics = YearMetricsService(current_year_payouts,
                                                       EmploymentService.get_employment_from_current_year(employments),
                                                       get_current_year(),
                                                       self.last_year_metrics).get_metrics_by_company()

    def get_metrics(self):
        """
            Get all metrics
        """
        companies_metrics = self._merge_companies_values()

        last_year_total, ytd_total, projected_total = self._get_total(companies_metrics)
        result = {}

        for key, _ in ALL_KEYS:
            result[key] = {
                'last_year_total': last_year_total[key],
                "ytd_total": ytd_total[key],
                "projected_total": projected_total[key],
                "companies": companies_metrics[key]
            }

        return result

    def _get_value(self, key: str, data):
        """
            Get value from data by key.
            Special case for pay_frequency, that is a set
        """
        if key == 'pay_frequency':
            value = getattr(data, key, Decimal(0))
            return {getattr(data, key)} if value else set()
        else:
            return getattr(data, key, Decimal(0))

    def _merge_companies_values(self) -> dict:
        """
        Merge last year and current year company metrics
        We want to have this format:
        {
            "gross_pay" => {
                "google":{
                    'last_year_total': X,
                    'ytd_total': X,
                    'projected_total':X,
                },
                "amazon":{
                    'last_year_total': X,
                    'ytd_total': X,
                    'projected_total':X,
                }
                ...
            }
            ...
        }

        """

        companies_metrics = {}

        companies = set(list(self.last_year_metrics.keys()) + list(self.current_year_metrics.keys()))

        for company in companies:
            last_year_metrics = self.last_year_metrics[company] if company in self.last_year_metrics else []
            current_year_metrics = self.current_year_metrics[
                company] if company in self.current_year_metrics else []
            projected_metrics = ProjectedIncomeMetrics(
                current_year_metrics) if company in self.current_year_metrics else []

            for key, default in ALL_KEYS:
                if key not in companies_metrics:
                    companies_metrics[key] = {}

                last_year_value = self._get_value(key, last_year_metrics)
                current_year_value = self._get_value(key, current_year_metrics)
                projected_total = self._get_value(key, projected_metrics)

                if not company in companies_metrics[key]:
                    companies_metrics[key][company] = {}
                companies_metrics[key][company]['last_year_total'] = last_year_value
                companies_metrics[key][company]['ytd_total'] = current_year_value
                companies_metrics[key][company]['projected_total'] = projected_total

        return companies_metrics

    def _calculate_total(self, key, total, new_value):
        """
            Calculate total for specific total (last year total, YTD total, projected total) by key
        """
        if key == 'pay_frequency':
            total[key] = total[key].union(new_value)
        elif key == 'total_days':
            # Total days are calculated by maximum value
            if not total[key] or new_value > total[key]:
                total[key] = new_value
        else:
            # The basic calculations - sum values
            total[key] += new_value

        return total

    def _get_total(self, companies_metrics: dict) -> Tuple[dict, dict, dict]:
        """
        Calculate total for last year, current year and projected based on companies metrics
        """
        last_year_total = {}
        ytd_total = {}
        projected_total = {}

        active_companies = len(list(self.active_employers))

        for key, default in ALL_KEYS:
            if key not in last_year_total:
                last_year_total[key] = default
                ytd_total[key] = default
                projected_total[key] = default

            metrics = companies_metrics[key]

            for company_name, metric in metrics.items():
                # Other numbers
                if metric['last_year_total']:
                    last_year_total = self._calculate_total(key, last_year_total, metric['last_year_total'])

                if metric['ytd_total']:
                    ytd_total = self._calculate_total(key, ytd_total, metric['ytd_total'])

                if metric['projected_total']:
                    projected_total = self._calculate_total(key, projected_total, metric['projected_total'])

        # Total for rate_of_pay should be an average "rate_of_pay" values from active_companies
        last_year_total['rate_of_pay'] = last_year_total[
                                             'rate_of_pay'] / active_companies if active_companies else Decimal(0)
        ytd_total['rate_of_pay'] = ytd_total['rate_of_pay'] / active_companies if active_companies else Decimal(0)
        projected_total['rate_of_pay'] = projected_total[
                                             'rate_of_pay'] / active_companies if active_companies else Decimal(0)

        return last_year_total, ytd_total, projected_total
