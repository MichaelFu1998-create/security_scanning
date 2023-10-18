def signed_number(number, precision=2):
    """
    Return the given number as a string with a sign in front of it, ie. `+` if the number is positive, `-` otherwise.
    """
    prefix = '' if number <= 0 else '+'
    number_str = '{}{:.{precision}f}'.format(prefix, number, precision=precision)

    return number_str