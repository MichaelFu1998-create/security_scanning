def percentage(self, value, *args):
        """ Return percentage value
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        n = int(n * 100.0)
        u = '%'
        return utility.with_unit(n, u)