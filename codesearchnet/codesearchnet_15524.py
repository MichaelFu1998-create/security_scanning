def hsl(self, *args):
        """ Translate hsl(...) to color string
        raises:
            ValueError
        returns:
            str
        """
        if len(args) == 4:
            return self.hsla(*args)
        elif len(args) == 3:
            h, s, l = args
            rgb = colorsys.hls_to_rgb(
                int(h) / 360.0, utility.pc_or_float(l), utility.pc_or_float(s))
            color = (utility.convergent_round(c * 255) for c in rgb)
            return self._rgbatohex(color)
        raise ValueError('Illegal color values')