def add(self, *args):
        """ Add integers
        args:
            args (list): target
        returns:
            str
        """
        if (len(args) <= 1):
            return 0
        return sum([int(v) for v in args])