def add_years(d, years_int):
        """
        adds number of years to a date
        :param BaseDateFloat d: date to add years to
        :param int years_int: number of years to add
        :return BaseDate: resulting date
        """

        y, m, d = BaseDate.to_ymd(d)
        if not is_leap_year(years_int) and m == 2:
            d = min(28, d)
        return BaseDateFloat.from_ymd(y + years_int, m, d)