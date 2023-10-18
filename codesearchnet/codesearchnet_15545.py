def away_from_zero_round(value, ndigits=0):
    """Round half-way away from zero.

    Python2's round() method.
    """
    if sys.version_info[0] >= 3:
        p = 10**ndigits
        return float(math.floor((value * p) + math.copysign(0.5, value))) / p
    else:
        return round(value, ndigits)