def is_business_day(self, holiday_obj=None):
        """
        :param list holiday_obj : datetime.date list defining business holidays
        :return: bool

        method to check if a date falls neither on weekend nor is holiday
        """
        y, m, d = BusinessDate.to_ymd(self)
        if weekday(y, m, d) > FRIDAY:
            return False
        holiday_list = holiday_obj if holiday_obj is not None else DEFAULT_HOLIDAYS
        if self in holiday_list:
            return False
        elif date(y, m, d) in holiday_list:
            return False
        return True