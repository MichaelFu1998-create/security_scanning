def human(self, size, base=1000, units=' kMGTZ'):
        """Convert the input ``size`` to human readable, short form."""
        sign = '+' if size >= 0 else '-'
        size = abs(size)
        if size < 1000:
            return '%s%d' % (sign, size)
        for i, suffix in enumerate(units):
            unit = 1000 ** (i + 1)
            if size < unit:
                return ('%s%.01f%s' % (
                    sign,
                    size / float(unit) * base,
                    suffix,
                )).strip()
        raise OverflowError