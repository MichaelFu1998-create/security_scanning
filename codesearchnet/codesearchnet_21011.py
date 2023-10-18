def add_period(self, p, holiday_obj=None):
        """
        addition of a period object

        :param BusinessDate d:
        :param p:
        :type p: BusinessPeriod or str
        :param list holiday_obj:
        :return bankdate:
        """

        if isinstance(p, (list, tuple)):
            return [BusinessDate.add_period(self, pd) for pd in p]
        elif isinstance(p, str):
            period = BusinessPeriod(p)
        else:
            period = p

        res = self
        res = BusinessDate.add_months(res, period.months)
        res = BusinessDate.add_years(res, period.years)
        res = BusinessDate.add_days(res, period.days)

        if period.businessdays:
            if holiday_obj:
                res = BusinessDate.add_business_days(res, period.businessdays, holiday_obj)
            else:
                res = BusinessDate.add_business_days(res, period.businessdays, period.holiday)

        return res