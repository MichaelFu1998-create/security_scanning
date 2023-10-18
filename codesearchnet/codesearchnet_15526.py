def hue(self, color, *args):
        """ Return the hue value of a color
        args:
            color (str): color
        raises:
            ValueError
        returns:
            float
        """
        if color:
            h, l, s = self._hextohls(color)
            return utility.convergent_round(h * 360.0, 3)
        raise ValueError('Illegal color values')