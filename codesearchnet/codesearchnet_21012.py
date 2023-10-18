def add_months(self, month_int):
        """
        addition of a number of months

        :param BusinessDate d:
        :param int month_int:
        :return bankdate:
        """

        month_int += self.month
        while month_int > 12:
            self = BusinessDate.add_years(self, 1)
            month_int -= 12
        while month_int < 1:
            self = BusinessDate.add_years(self, -1)
            month_int += 12
        l = monthrange(self.year, month_int)[1]
        return BusinessDate.from_ymd(self.year, month_int, min(l, self.day))