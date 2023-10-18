def number_range_inclusive(min, max, type=float):
    """
    Return a value check function which raises a ValueError if the supplied
    value when cast as `type` is less than `min` or greater than `max`.

    """

    def checker(v):
        if type(v) < min or type(v) > max:
            raise ValueError(v)
    return checker