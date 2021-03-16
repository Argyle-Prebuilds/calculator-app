from decimal import Decimal
from api.utils.dates import get_date_from_str
from users.services.income_metrics.employment_service import get_current_month_number
from users.services.income_months.income_months import LAST_YEAR_TYPE, CURRENT_YEAR_TYPE, IncomeMonths, PROJECTED_TYPE, \
    PROJECTED_STDEV_TYPE, PROJECTED_STDEV_UPPER_TYPE, PROJECTED_STDEV_LOWER_TYPE, YTD_TYPE

import statistics


class IncomeMonthService:
    """
        Income Month Service - prepare all gross pay values for last year, current year and projected, grouped by months
    """

    def __init__(self, last_year_payouts: list, current_year_payouts: list):
        self.last_year_payouts = last_year_payouts
        self.current_year_payouts = current_year_payouts

        self.metrics = {}
        for income_type, payouts in ((LAST_YEAR_TYPE, last_year_payouts), (CURRENT_YEAR_TYPE, current_year_payouts)):
            for payout in payouts:
                payout_date = get_date_from_str(payout['payout_date'])
                key = f"{payout_date.year}_{payout_date.month}"
                if key not in self.metrics:
                    self.metrics[key] = IncomeMonths(payout_date, income_type)

                self.metrics[key].add_income(payout['gross_pay'])

    def _calculate_projected_month_gross_pay(self, result) -> dict:
        """
            Projected per month is an average using the previous months gross pay
            January - January YTD
            February - average of January-February gross pays
            March - average of January-March gross pays
        """
        projected = {}
        gross_sum = 0
        count = 0
        current_month = get_current_month_number()

        for month in range(1, 13):
            if month in result[CURRENT_YEAR_TYPE]:
                current_year_month_gross = result[CURRENT_YEAR_TYPE][month]
                gross_sum += current_year_month_gross
                count += 1

                projected[month] = current_year_month_gross if month < current_month else gross_sum / count
            else:
                projected[month] = 0 if month < current_month else gross_sum / count

        return projected

    def _calculate_projected_stdev(self, result):
        """
            Projected standard deviation is take into account last year and YTD values.
            For example:
            January - stdev from last year income + January income
            February - stdev from last year income + January income + February income
        """
        values = list(result[LAST_YEAR_TYPE].values())
        projected_stdev = {}

        for month in range(1, 13):
            if month in result[CURRENT_YEAR_TYPE]:
                current_year_month_gross = result[CURRENT_YEAR_TYPE][month]
                values.append(current_year_month_gross)
            projected_stdev[month] = round(statistics.stdev(values), 2)

        return projected_stdev

    def convert_to_chart_values(self, data):
        """
        Convert data to expected format. Data is shift by one month. It means for January chart should dislay 0, for February - January value.
        """

        converted = {}

        for key, value in data.items():
            all_values = list(value.values())
            converted[key] = [0] + all_values[:-1] if key == CURRENT_YEAR_TYPE else [0] + all_values

        return converted

    def get_metrics(self):
        """
            All gross pay values for last year, current year and projected, grouped by months
        """
        current_month = get_current_month_number()
        all_metrics = self.metrics.values()

        result = {
            LAST_YEAR_TYPE: {month: Decimal(0) for month in range(1, 13)},
            CURRENT_YEAR_TYPE: {month: Decimal(0) for month in range(1, current_month + 1)},
        }

        for metrics in all_metrics:
            result[metrics.income_type][metrics.month] = Decimal(round(metrics.income_value, 2))

        # result[YTD_TYPE] = self._calculate_projected_month_gross_pay(result)
        # Projected
        result[PROJECTED_TYPE] = self._calculate_projected_month_gross_pay(result)
        result[PROJECTED_STDEV_TYPE] = self._calculate_projected_stdev(result)
        result[PROJECTED_STDEV_UPPER_TYPE] = {month: result[PROJECTED_TYPE][month] + result[PROJECTED_STDEV_TYPE][month]
                                              for month in range(1, 13)}
        result[PROJECTED_STDEV_LOWER_TYPE] = {month: result[PROJECTED_TYPE][month] - result[PROJECTED_STDEV_TYPE][month]
                                              for month in range(1, 13)}

        return result
