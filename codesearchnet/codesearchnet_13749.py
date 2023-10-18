def interest_accrued(self, valuation_date):
        """
        interest_accrued
        :param valuation_date:
        :type valuation_date:
        :return:
        :rtype:
        """
        return sum([l.interest_accrued(valuation_date) for l in self.legs if hasattr(l, 'interest_accrued')])