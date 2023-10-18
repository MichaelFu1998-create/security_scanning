def from_ymd_to_excel(year, month, day):
    """
    converts date as `(year, month, day)` tuple into Microsoft Excel representation style

    :param tuple(int, int, int): int tuple `year, month, day`
    :return int:
    """
    if not is_valid_ymd(year, month, day):
        raise ValueError("Invalid date {0}.{1}.{2}".format(year, month, day))

    days = _cum_month_days[month - 1] + day
    days += 1 if (is_leap_year(year) and month > 2) else 0

    years_distance = year - 1900
    days += years_distance * 365 + \
            (years_distance + 3) // 4 - (years_distance + 99) // 100 + (years_distance + 299) // 400

    # count days since 30.12.1899 (excluding 30.12.1899) (workaround for excel bug)
    days += 1 if (year, month, day) > (1900, 2, 28) else 0
    return days