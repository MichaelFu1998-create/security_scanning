def diff(self, end_date):
        """
        difference expressed as a tuple of years, months, days
        (see also the python lib dateutils.relativedelta)

        :param BusinessDate start_date:
        :param BusinessDate end_date:
        :return (int, int, int):
        """

        if end_date < self:
            y, m, d = BusinessDate.diff(end_date, self)
            return -y, -m, -d
        y = end_date.year - self.year
        m = end_date.month - self.month

        while m < 0:
            y -= 1
            m += 12
        while m > 12:
            y += 1
            m -= 12

        s = BusinessDate.add_years(BusinessDate.add_months(self, m), y)
        d = BusinessDate.diff_in_days(s, end_date)

        if d < 0:
            m -= 1
            if m < 0:
                y -= 1
                m += 12
            s = BusinessDate.add_years(BusinessDate.add_months(self, m), y)

        d = BusinessDate.diff_in_days(s, end_date)

        return -int(y), -int(m), -int(d)