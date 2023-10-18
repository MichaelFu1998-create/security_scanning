def round(self, value, *args):
        """ Round number
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(
            int(utility.away_from_zero_round(float(n))), u)