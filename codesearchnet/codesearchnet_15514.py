def increment(self, value, *args):
        """ Increment function
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(n + 1, u)