def ceil(self, value, *args):
        """ Ceil number
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(int(math.ceil(n)), u)