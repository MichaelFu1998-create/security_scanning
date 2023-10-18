def argb(self, *args):
        """ Translate argb(...) to color string

        Creates a hex representation of a color in #AARRGGBB format (NOT
        #RRGGBBAA!). This format is used in Internet Explorer, and .NET
        and Android development.

        raises:
            ValueError
        returns:
            str
        """
        if len(args) == 1 and type(args[0]) is str:
            match = re.match(r'rgba\((.*)\)', args[0])
            if match:
                # NOTE(saschpe): Evil hack to cope with rgba(.., .., .., 0.5) passed through untransformed
                rgb = re.sub(r'\s+', '', match.group(1)).split(',')
            else:
                rgb = list(self._hextorgb(args[0]))
        else:
            rgb = list(args)
        if len(rgb) == 3:
            return self._rgbatohex([255] + list(map(int, rgb)))
        elif len(rgb) == 4:
            rgb = [rgb.pop()] + rgb  # Move Alpha to front
            try:
                fval = float(list(rgb)[0])
                if fval > 1:
                    rgb = [255] + rgb[1:]  # Clip invalid integer/float values
                elif 1 >= fval >= 0:
                    rgb = [
                        fval * 256
                    ] + rgb[1:]  # Convert 0-1 to 0-255 range for _rgbatohex
                else:
                    rgb = [0] + rgb[1:]  # Clip lower bound
                return self._rgbatohex(list(map(int, rgb)))
            except ValueError:
                if all((a for a in rgb
                        if a[-1] == '%' and 100 >= int(a[:-1]) >= 0)):
                    return self._rgbatohex(
                        [int(a[:-1]) * 255 / 100.0 for a in rgb])
        raise ValueError('Illegal color values')