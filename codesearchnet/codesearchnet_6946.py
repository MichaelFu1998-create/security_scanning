def _round_whole_even(i):
    r'''Round a number to the nearest whole number. If the number is exactly
    between two numbers, round to the even whole number. Used by
    `viscosity_index`.

    Parameters
    ----------
    i : float
        Number, [-]

    Returns
    -------
    i : int
        Rounded number, [-]

    Notes
    -----
    Should never run with inputs from a practical function, as numbers on
    computers aren't really normally exactly between two numbers.

    Examples
    --------
    _round_whole_even(116.5)
    116
    '''
    if i % .5 == 0:
        if (i + 0.5) % 2 == 0:
            i = i + 0.5
        else:
            i = i - 0.5
    else:
        i = round(i, 0)
    return int(i)