def saturation(self, color, *args):
        """ Return the saturation value of a color
        args:
            color (str): color
        raises:
            ValueError
        returns:
            float
        """
        if color:
            h, l, s = self._hextohls(color)
            return s * 100.0
        raise ValueError('Illegal color values')