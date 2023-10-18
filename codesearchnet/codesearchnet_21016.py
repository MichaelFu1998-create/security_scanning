def get_act_act(self, end):
        """
            implements Act/Act day count convention (4.16(b) 2006 ISDA Definitions)
        """
        # split end-self in year portions

        # if the period does not lie within a year split the days in the period as following:
        #           restdays of start year / years in between / days in the end year
        # REMARK: following the affore mentioned ISDA Definition the first day of the period is included whereas the
        # last day will be excluded
        # What remains to check now is only whether the start and end year are leap or non-leap years. The quotients
        # can be easily calculated and for the years in between they are always one (365/365 = 1; 366/366 = 1)

        if end.year - self.year == 0:
            if BusinessDate.is_leap_year(self.year):
                return BusinessDate.diff_in_days(self, end) / 366.0  # leap year: 366 days
            else:
                # return BusinessDate.diff_in_days(self, end) / 366.0
                return BusinessDate.diff_in_days(self, end) / 365.0  # non-leap year: 365 days
        else:
            rest_year1 = BusinessDate.diff_in_days(self, BusinessDate(
                date(self.year, 12, 31))) + 1  # since the first day counts

            rest_year2 = abs(BusinessDate.diff_in_days(end, BusinessDate(
                date(end.year, 1, 1))))  # here the last day is automatically not counted

            years_in_between = end.year - self.year - 1

            return years_in_between + rest_year1 / (366.0 if is_leap_year(self.year) else 365.0) + rest_year2 / (
                366.0 if is_leap_year(end.year) else 365.0)