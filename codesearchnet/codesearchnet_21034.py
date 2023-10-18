def add_years(date_obj, years_int):
        """
        addition of a number of years

        :param BaseDateTuple d:
        :param int years_int:
        :return BaseDatetimeDate:
        """
        y, m, d = BaseDateTuple.to_ymd(date_obj)
        y += years_int
        if not is_leap_year(y) and m == 2:
            d = min(28, d)
        return BaseDateTuple.from_ymd(y, m, d)