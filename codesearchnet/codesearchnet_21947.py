def frexp10(x):
    """
    Finds the mantissa and exponent of a number :math:`x` such that :math:`x = m 10^e`.

    Parameters
    ----------

    x : float
        Number :math:`x` such that :math:`x = m 10^e`.

    Returns
    -------

    mantissa : float
        Number :math:`m` such that :math:`x = m 10^e`.
    exponent : float
        Number :math:`e` such that :math:`x = m 10^e`.
    """
    expon = _np.int(_np.floor(_np.log10(_np.abs(x))))
    mant = x/_np.power(10, expon)
    return (mant, expon)