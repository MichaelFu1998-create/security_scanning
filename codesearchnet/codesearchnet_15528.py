def lighten(self, color, diff, *args):
        """ Lighten a color
        args:
            color (str): color
            diff (str): percentage
        returns:
            str
        """
        if color and diff:
            return self._ophsl(color, diff, 1, operator.add)
        raise ValueError('Illegal color values')