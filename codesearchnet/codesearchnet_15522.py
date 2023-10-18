def rgba(self, *args):
        """ Translate rgba(...) to color string
        raises:
            ValueError
        returns:
            str
        """
        if len(args) == 4:
            try:
                falpha = float(list(args)[3])
                if falpha > 1:
                    args = args[:3]
                if falpha == 0:
                    values = self._rgbatohex_raw(list(map(int, args)))
                    return "rgba(%s)" % ','.join([str(a) for a in values])
                return self._rgbatohex(list(map(int, args)))
            except ValueError:
                if all((a for a in args
                        if a[-1] == '%' and 100 >= int(a[:-1]) >= 0)):
                    alpha = list(args)[3]
                    if alpha[-1] == '%' and float(alpha[:-1]) == 0:
                        values = self._rgbatohex_raw(
                            [int(a[:-1]) * 255 / 100.0 for a in args])
                        return "rgba(%s)" % ','.join([str(a) for a in values])
                    return self._rgbatohex(
                        [int(a[:-1]) * 255 / 100.0 for a in args])
        raise ValueError('Illegal color values')