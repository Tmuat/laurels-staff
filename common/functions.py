from django.utils import timezone


def quarter_year_calc():
    def calculate_start_month(date):
        start_month = (((date.month - 1) // 3) * 3) + 1
        return start_month

    def calculate_start_year(date):
        start_year = date.year
        return start_year

    todays_date = timezone.now()

    start_month = int(calculate_start_month(todays_date))
    start_year = int(calculate_start_year(todays_date))

    if start_month == 10:
        start_year + 1

    return str(start_year)
