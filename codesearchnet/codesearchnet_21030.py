def add_days(d, days_int):
        """
        addition of a number of days

        :param BaseDateDatetimeDate d:
        :param int days_int:
        :return BaseDatetimeDate:
        """
        n = date(d.year, d.month, d.day) + timedelta(days_int)
        return BaseDateDatetimeDate(n.year, n.month, n.day)