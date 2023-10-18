def add_business_days(self, days_int, holiday_obj=None):
        """
        private method for the addition of business days, used in the addition of a BusinessPeriod only

        :param BusinessDate d:
        :param int days_int:
        :param list holiday_obj:
        :return: BusinessDate
        """

        res = self
        if days_int >= 0:
            count = 0
            while count < days_int:
                res = BusinessDate.add_days(res, 1)
                if BusinessDate.is_business_day(res, holiday_obj):
                    count += 1
        else:
            count = 0
            while count > days_int:
                res = BusinessDate.add_days(res, -1)
                if BusinessDate.is_business_day(res, holiday_obj):
                    count -= 1

        return res