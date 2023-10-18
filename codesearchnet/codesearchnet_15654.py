def from_decimal(number, width=1):
    """
    Takes a decimal and returns base91 char string.
    With optional parameter for fix with output
    """
    text = []

    if not isinstance(number, int_type):
        raise TypeError("Expected number to be int, got %s", type(number))
    elif not isinstance(width, int_type):
        raise TypeError("Expected width to be int, got %s", type(number))
    elif number < 0:
        raise ValueError("Expected number to be positive integer")
    elif number > 0:
        max_n = ceil(log(number) / log(91))

        for n in _range(int(max_n), -1, -1):
            quotient, number = divmod(number, 91**n)
            text.append(chr(33 + quotient))

    return "".join(text).lstrip('!').rjust(max(1, width), '!')