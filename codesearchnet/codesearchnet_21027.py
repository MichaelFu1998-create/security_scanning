def from_excel_to_ymd(excel_int):
    """
    converts date in Microsoft Excel representation style and returns `(year, month, day)` tuple

    :param int excel_int: date as int (days since 1899-12-31)
    :return tuple(int, int, int):
    """

    int_date = int(floor(excel_int))
    int_date -= 1  if excel_int > 60 else 0
    # jan dingerkus: There are two errors in excels own date <> int conversion.
    # The first is that there exists the 00.01.1900 and the second that there never happend to be a 29.2.1900 since it
    # was no leap year. So there is the int 60 <> 29.2.1900 which has to be jumped over.

    year = (int_date - 1) // 365
    rest_days = int_date - 365 * year - (year + 3) // 4 + (year + 99) // 100 - (year + 299) // 400
    year += 1900

    while rest_days <= 0:
        year -= 1
        rest_days += days_in_year(year)

    month = 1
    if is_leap_year(year) and rest_days == 60:
        month = 2
        day = 29
    else:
        if is_leap_year(year) and rest_days > 60:
            rest_days -= 1

        while rest_days > _cum_month_days[month]:
            month += 1

        day = rest_days - _cum_month_days[month - 1]
    return year, month, day