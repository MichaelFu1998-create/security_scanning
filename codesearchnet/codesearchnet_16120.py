def number_range_exclusive(min, max, type=float):
    """
    Return a value check function which raises a ValueError if the supplied
    value when cast as `type` is less than or equal to `min` or greater than
    or equal to `max`.

    """

    def checker(v):
        if type(v) <= min or type(v) >= max:
            raise ValueError(v)
    return checker