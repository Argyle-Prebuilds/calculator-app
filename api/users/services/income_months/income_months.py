import datetime
from decimal import Decimal

LAST_YEAR_TYPE = 'LAST_YEAR'
YTD_TYPE = 'YTD'
CURRENT_YEAR_TYPE = 'CURRENT_YEAR'
PROJECTED_TYPE = 'PROJECTED'
PROJECTED_STDEV_TYPE = 'PROJECTED_STDEV'
PROJECTED_STDEV_UPPER_TYPE = 'PROJECTED_STDEV_UPPER'
PROJECTED_STDEV_LOWER_TYPE = 'PROJECTED_STDEV_LOWER'


class IncomeMonths:
    income_value: Decimal
    income_type: int
    month: int
    year: int

    def __init__(self, date: datetime.date, income_type: int):
        self.income_value = Decimal(0)
        self.month = date.month
        self.year = date.year
        self.income_type = income_type

    def add_income(self, value: float):
        self.income_value += Decimal(value)
