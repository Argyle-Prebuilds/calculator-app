import datetime
from api.utils.dates import get_date_from_str


def get_current_year():
    return datetime.datetime.now().year


def get_current_month_number():
    return datetime.datetime.now().month


class EmploymentService:

    @staticmethod
    def filter_employments_by_dates(employment, from_date: datetime.date, to_date: datetime.date) -> bool:
        hire_datetime = get_date_from_str(employment['hire_datetime'])
        termination_datetime = employment['termination_datetime']

        if employment['termination_datetime']:
            termination_datetime = get_date_from_str(termination_datetime)

        if not termination_datetime:
            return hire_datetime <= to_date

        if hire_datetime <= to_date and termination_datetime >= from_date:
            return True

        return False

    @staticmethod
    def get_employment_from_last_year(employments):
        current_year = get_current_year()
        from_date = datetime.date(current_year - 1, 1, 1)
        to_date = datetime.date(current_year - 1, 12, 31)

        return filter(lambda employment: EmploymentService.filter_employments_by_dates(employment, from_date, to_date),
                      employments)

    @staticmethod
    def get_employment_from_current_year(employments):
        current_year = get_current_year()
        from_date = datetime.date(current_year, 1, 1)
        to_date = datetime.date.today()

        return filter(lambda employment: EmploymentService.filter_employments_by_dates(employment, from_date, to_date),
                      employments)

    @staticmethod
    def get_active_employers(employments):
        from_date = datetime.date.today()
        to_date = datetime.date.today()

        return filter(lambda employment: EmploymentService.filter_employments_by_dates(employment, from_date, to_date),
                      employments)
