def is_valid_ymd(year, month, day):
    """
    return True if (year,month, day) can be represented in Excel-notation
    (number of days since 30.12.1899) for calendar days, otherwise False

    :param int year: calendar year
    :param int month: calendar month
    :param int day: calendar day
    :return bool:
    """

    return 1 <= month <= 12 and 1 <= day <= days_in_month(year, month) and year >= 1899