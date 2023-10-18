def get_percentage(a, b, i=False, r=False):
    """
    Finds the percentage of one number over another.

    Args:
        a: The number that is a percent, int or float.

        b: The base number that a is a percent of, int or float.

        i: Optional boolean integer. True if the user wants the result returned as
        a whole number. Assumes False.

        r: Optional boolean round. True if the user wants the result rounded.
        Rounds to the second decimal point on floating point numbers. Assumes False.

    Returns:
        The argument a as a percentage of b. Throws a warning if integer is set to True
        and round is set to False.
    """
    # Round to the second decimal
    if i is False and r is True:
        percentage = round(100.0 * (float(a) / b), 2)

    # Round to the nearest whole number
    elif (i is True and r is True) or (i is True and r is False):
        percentage = int(round(100 * (float(a) / b)))

        # A rounded number and an integer were requested
        if r is False:
            warnings.warn(
                "If integer is set to True and Round is set to False, you will still get a rounded number if you pass floating point numbers as arguments."
            )

    # A precise unrounded decimal
    else:
        percentage = 100.0 * (float(a) / b)

    return percentage