def convergent_round(value, ndigits=0):
    """Convergent rounding.

    Round to neareas even, similar to Python3's round() method.
    """
    if sys.version_info[0] < 3:
        if value < 0.0:
            return -convergent_round(-value)

        epsilon = 0.0000001
        integral_part, _ = divmod(value, 1)

        if abs(value - (integral_part + 0.5)) < epsilon:
            if integral_part % 2.0 < epsilon:
                return integral_part
            else:
                nearest_even = integral_part + 0.5
                return math.ceil(nearest_even)
    return round(value, ndigits)