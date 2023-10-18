def add_days(date_obj, days_int):
        """
        addition of a number of days

        :param BaseDateTuple d:
        :param int days_int:
        :return BaseDatetimeDate:
        """
        n = from_ymd_to_excel(*date_obj.date) + days_int

        return BaseDateTuple(*from_excel_to_ymd(n))