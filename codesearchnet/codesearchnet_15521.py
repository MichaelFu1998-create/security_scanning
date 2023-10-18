def rgb(self, *args):
        """ Translate rgb(...) to color string
        raises:
            ValueError
        returns:
            str
        """
        if len(args) == 4:
            args = args[:3]
        if len(args) == 3:
            try:
                return self._rgbatohex(list(map(int, args)))
            except ValueError:
                if all((a for a in args
                        if a[-1] == '%' and 100 >= int(a[:-1]) >= 0)):
                    return self._rgbatohex(
                        [int(a[:-1]) * 255 / 100.0 for a in args])
        raise ValueError('Illegal color values')