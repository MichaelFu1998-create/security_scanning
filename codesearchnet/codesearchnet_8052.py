def between(a, b, inclusive_min=True, inclusive_max=True):
    """
    Indicate that value is a numeric range
    """
    return RangeValue(a, b,
                      inclusive_min=inclusive_min, inclusive_max=inclusive_max)