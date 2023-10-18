def diff_in_days(start, end):
        """
        calculate difference between given dates in days

        :param BaseDateTuple start: state date
        :param BaseDateTuple end: end date
        :return float: difference between end date and start date in days
        """

        diff = from_ymd_to_excel(*end.date)-from_ymd_to_excel(*start.date)
        return float(diff)