def from_date(datetime_date):
        """
        construct BusinessDate instance from datetime.date instance,
        raise ValueError exception if not possible

        :param datetime.date datetime_date: calendar day
        :return bool:
        """
        return BusinessDate.from_ymd(datetime_date.year, datetime_date.month, datetime_date.day)