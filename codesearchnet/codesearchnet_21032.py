def diff_in_days(start, end):
        """
        calculate difference between given dates in days

        :param BaseDateDatetimeDate start: state date
        :param BaseDateDatetimeDate end: end date
        :return float: difference between end date and start date in days
        """
        diff = date(end.year, end.month, end.day) - date(start.year, start.month, start.day)
        return float(diff.days)