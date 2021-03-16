import datetime


class DateService:

    @staticmethod
    def calculate_projected_days_in_year(hire_datetime: datetime.date, termination_datetime: datetime.date or None,
                                         year: int) -> int:
        """
        Calculate how many days employee will work in specific year (projected days)

        @param hire_datetime:  datetime.date
        @param termination_datetime:  datetime.date or None
        @param year: int

        Example 1:
        hire_datetime= 2019-10-20
        termination_datetime = None
        year = 2021

        result = 365 # Probably employee will work all year

        Example 2:
        hire_datetime= 2019-10-20
        termination_datetime = 2021-01-30
        year = 2021

        result = 30

        More examples in tests.py

        :return: int
        """
        start_date = hire_datetime
        end_date = termination_datetime

        if end_date is None:
            end_date = datetime.date(year, 12, 31)

        elif end_date.year > year:
            end_date = datetime.date(year, 12, 31)

        if hire_datetime.year < year:
            start_date = datetime.date(year, 1, 1)

        return (end_date - start_date).days + 1

    @staticmethod
    def calculate_work_days_in_year(hire_datetime: datetime.date, termination_datetime: datetime.date or None,
                                    year: int) -> int:
        """
        Calculate how many days employee worked in specific year
        @param hire_datetime:  datetime.date
        @param termination_datetime:  datetime.date or None
        @param year: int

        Example 1:
        hire_datetime= 2019-10-20
        termination_datetime = None
        year = 2021

        today = 28-01-2021

        result = 28

        Example 2:
        hire_datetime= 2021-01-02
        termination_datetime = 2021-01-26
        year = 2021

        result = 25

        More examples in tests.py

        :return: int
        """
        start_date = hire_datetime
        end_date = termination_datetime
        today = datetime.date.today()

        if end_date is None:
            if today.year == year:
                end_date = today

            # today 2021 but we calculate for year 2020
            elif today.year > year:
                end_date = datetime.date(year, 12, 31)

        elif end_date.year > year:
            end_date = datetime.date(year, 12, 31)

        if hire_datetime.year < year:
            start_date = datetime.date(year, 1, 1)

        return (end_date - start_date).days + 1
