def add_years(d, years_int):
        """
        addition of a number of years

        :param BaseDateDatetimeDate d:
        :param int years_int:
        :return BaseDatetimeDate:
        """
        y, m, d = BaseDateDatetimeDate.to_ymd(d)
        y += years_int
        if not is_leap_year(y) and m == 2:
            d = min(28, d)
        return BaseDateDatetimeDate.from_ymd(y, m, d)