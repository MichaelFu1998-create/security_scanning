def darken(self, color, diff, *args):
        """ Darken a color
        args:
            color (str): color
            diff (str): percentage
        returns:
            str
        """
        if color and diff:
            return self._ophsl(color, diff, 1, operator.sub)
        raise ValueError('Illegal color values')