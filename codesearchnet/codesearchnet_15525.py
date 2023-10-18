def hsla(self, *args):
        """ Translate hsla(...) to color string
        raises:
            ValueError
        returns:
            str
        """
        if len(args) == 4:
            h, s, l, a = args
            rgb = colorsys.hls_to_rgb(
                int(h) / 360.0, utility.pc_or_float(l), utility.pc_or_float(s))
            color = [float(utility.convergent_round(c * 255)) for c in rgb]
            color.append(utility.pc_or_float(a))
            return "rgba(%s,%s,%s,%s)" % tuple(color)
        raise ValueError('Illegal color values')