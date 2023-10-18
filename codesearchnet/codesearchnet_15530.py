def spin(self, color, degree, *args):
        """ Spin color by degree. (Increase / decrease hue)
        args:
            color (str): color
            degree (str): percentage
        raises:
            ValueError
        returns:
            str
        """
        if color and degree:
            if isinstance(degree, string_types):
                degree = float(degree.strip('%'))
            h, l, s = self._hextohls(color)
            h = ((h * 360.0) + degree) % 360.0
            h = 360.0 + h if h < 0 else h
            rgb = colorsys.hls_to_rgb(h / 360.0, l, s)
            color = (utility.convergent_round(c * 255) for c in rgb)
            return self._rgbatohex(color)
        raise ValueError('Illegal color values')