def datetime_range_inclusive(min, max, format):
    """
    Return a value check function which raises a ValueError if the supplied
    value when converted to a datetime using the supplied `format` string is
    less than `min` or greater than `max`.

    """

    dmin = datetime.strptime(min, format)
    dmax = datetime.strptime(max, format)
    def checker(v):
        dv = datetime.strptime(v, format)
        if dv < dmin or dv > dmax:
            raise ValueError(v)
    return checker