import datetime
from abc import ABC, abstractmethod
from decimal import Decimal
from api.utils.dates import get_date_from_str
from users.services.income_metrics.date_service import DateService
from users.services.income_metrics.employment_service import get_current_month_number

PAYOUTS_KEYS = ['hours', 'overtime', 'commission', 'bonuses', 'reimbursements', 'gross_pay', 'deductions', 'net_pay',
                'taxes', 'payout_date']


class IncomeMetrics(ABC):
    """
    Abstract class, that define all attributes needed to calculations
    """
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    SEMI_MONTHLY = 'SEMI_MONTHLY'
    BIWEEKLY = 'BIWEEKLY'
    NO_INFORMATION = 'NO_INFORMATION'

    def __init__(self, year):
        self.year = year
        # All hours
        self.hours = Decimal(0)
        # Overtime Pay for a year
        self.overtime = Decimal(0)
        # Commission Pay for a year
        self.commission = Decimal(0)
        # Bonus Pay for a year
        self.bonuses = Decimal(0)
        # Other Pay for a year
        self.reimbursements = Decimal(0)
        # Total Pay for a year
        self.gross_pay = Decimal(0)
        # Other deductions
        self.deductions = Decimal(0)
        # Total Net
        self.net_pay = Decimal(0)  # net
        # Total taxes
        self.taxes = Decimal(0)  # taxes

        # Keep all payment dates
        self.payment_dates = []

        self.hire_date = None
        self.termination_date = None

    @property
    def hours_per_week(self):
        """
        Hours Worked per Week

        total_days = Termination Datetime - Hire Datetime
        total_weeks = total_days / 7
        hours_per_week = sum of yearly payouts.hours / total_weeks
        """

        total_weeks = int(self.total_days / 7)

        if self.total_days:
            return Decimal(round(self.hours / total_weeks, 2))

        return Decimal(0)

    @property
    def pay_frequency(self):
        """ Current/Latest Pay Frequency """

        intervals = []
        self.payment_dates.sort()
        payment_dates_number = len(self.payment_dates)
        for index in range(0, payment_dates_number - 1):
            interval = (self.payment_dates[index + 1] - self.payment_dates[index]).days
            intervals.append(interval)

        if not len(intervals):
            return None

        avg_interval = sum(intervals) / len(intervals)
        if 0 <= avg_interval <= 10:
            return self.WEEKLY
        elif avg_interval == 14:
            return self.BIWEEKLY
        elif 10 < avg_interval <= 21:
            return self.SEMI_MONTHLY
        elif 21 < avg_interval <= 40:
            return self.MONTHLY
        else:
            return None

    @property
    def base_pay(self):
        """
        Base Pay for a year
        Sum of yearly payouts.gross_pay - bonuses - reimbursements - overtime = Base Pay for a year
        """
        return self.gross_pay - self.bonuses - self.reimbursements - self.overtime

    @property
    def rate_of_pay(self):
        """
        Current/Latest Rate of Pay
        gross pay / sum of yearly payouts.hours
        """

        if self.hours:
            return Decimal(round(self.gross_pay / self.hours, 2))

        return Decimal(0)

    @property
    def total_days(self):
        # termination_date can be None
        if self.year and self.hire_date:
            days = DateService.calculate_work_days_in_year(self.hire_date, self.termination_date, self.year)
            return Decimal(days)
        return Decimal(0)

    @property
    @abstractmethod
    def gross_monthly(self):
        pass

    @property
    @abstractmethod
    def gross_monthly_with_last_year(self):
        pass

    def append_payment_date(self, hours: str, payment_date: str):
        """
        Append a payment date, only if hours number is greater than 0.
        If hours is equal to zero, it means this payout is responsible for bonuses or extra
        """
        if hours and float(hours) > 0 and payment_date:
            self.payment_dates.append(get_date_from_str(payment_date))

    def add_payout(self, payout):
        for key, value in payout.items():
            if key in PAYOUTS_KEYS:
                if key == 'payout_date':
                    if payout['hours'] and float(payout['hours']) > 0:
                        self.payment_dates.append(get_date_from_str(payout[key]))
                    continue

                current_value = getattr(self, key)
                if current_value is not None and value is not None:
                    setattr(self, key, current_value + Decimal(value))


class LastYearIncomeMetrics(IncomeMetrics):
    """
        Income metrics from one company from last year
    """

    @property
    def gross_monthly(self):
        """
        Parent Row: Monthly Gross income
        Last Year = Last year's values / 12
        """
        value = self.gross_pay / 12
        return Decimal(round(value, 2))

    @property
    def gross_monthly_with_last_year(self):
        """
        Child row: "Gross Monthly Income + 1-yr Avg"
        1. Last Year = Last year's values / 12 (no change from parent row)
        """
        value = self.gross_pay / 12
        return Decimal(round(value, 2))


class CurrentYearIncomeMetrics(LastYearIncomeMetrics):
    """
        Income metrics from one company from current year
    """

    def __init__(self, year):
        super().__init__(year)
        self.last_year_metrics = None

    def set_last_year_metrics(self, last_year_metrics):
        # Needed last year value to calculate gross monthly (Last year's values + YTD value)
        self.last_year_metrics = last_year_metrics

    @property
    def gross_monthly(self):
        """
        Parent Row: Monthly Gross income
        YTD Year = Current year's values / current month
        """
        value = self.gross_pay / get_current_month_number()
        return Decimal(round(value, 2))

    @property
    def gross_monthly_with_last_year(self):
        """
        Child row: "Gross Monthly Income + 1-yr Avg"
        2. YTD Avg = (Last year's values + YTD value) / (12 + months YTD)
        """
        months = get_current_month_number()

        if self.last_year_metrics:
            value = (self.last_year_metrics.gross_pay + self.gross_pay) / (12 + months)
            return Decimal(round(value, 2))

        value = self.gross_pay / (12 + months)
        return Decimal(round(value, 2))


class ProjectedIncomeMetrics:
    """
        This class calculate projected metrics base on current year metrics
        Important: if employer is not an actual_employer we return value 0.
    """

    def __init__(self, current_year_metrics: CurrentYearIncomeMetrics):
        self.current_year_metrics = current_year_metrics

        self.hire_date = current_year_metrics.hire_date
        self.termination_date = current_year_metrics.termination_date
        self.is_actual_employer = self._check_if_actual_employer()
        self.year = current_year_metrics.year
        self.gross_monthly = current_year_metrics.gross_monthly if self.is_actual_employer else Decimal(0)
        self.gross_monthly_with_last_year = current_year_metrics.gross_monthly_with_last_year if self.is_actual_employer else Decimal(
            0)
        self.hours_per_week = current_year_metrics.hours_per_week if self.is_actual_employer else Decimal(0)
        self.rate_of_pay = current_year_metrics.rate_of_pay if self.is_actual_employer else Decimal(0)
        self.pay_frequency = current_year_metrics.pay_frequency if self.is_actual_employer else Decimal(0)

    def _check_if_actual_employer(self):
        return (self.hire_date and self.termination_date is None) or (
                self.termination_date and self.termination_date > datetime.date.today())

    def _estimate_value(self, value):
        if not self.is_actual_employer:
            return Decimal(0)

        now = datetime.datetime.now()

        projected = value / now.month * 12
        return Decimal(round(projected, 2))

    @property
    def total_days(self):
        # termination_date can be None
        if self.year and self.hire_date:
            days = DateService.calculate_projected_days_in_year(self.hire_date, self.termination_date, self.year)
            return Decimal(days)
        return Decimal(0)

    @property
    def base_pay(self):
        return self._estimate_value(self.current_year_metrics.base_pay)

    @property
    def overtime(self):
        return self._estimate_value(self.current_year_metrics.overtime)

    @property
    def commission(self):
        return self._estimate_value(self.current_year_metrics.commission)

    @property
    def bonuses(self):
        return self._estimate_value(self.current_year_metrics.bonuses)

    @property
    def reimbursements(self):
        return self._estimate_value(self.current_year_metrics.reimbursements)

    @property
    def gross_pay(self):
        return self._estimate_value(self.current_year_metrics.gross_pay)

    @property
    def deductions(self):
        return self._estimate_value(self.current_year_metrics.deductions)

    @property
    def net_pay(self):
        return self._estimate_value(self.current_year_metrics.net_pay)

    @property
    def taxes(self):
        return self._estimate_value(self.current_year_metrics.taxes)
