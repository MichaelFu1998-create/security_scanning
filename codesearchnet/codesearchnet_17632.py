def Sh(L: float, h: float, D: float) -> float:
    """
    Calculate the Sherwood number.

    :param L: [m] mass transfer surface characteristic length.
    :param h: [m/s] mass transfer coefficient.
    :param D: [m2/s] fluid mass diffusivity.

    :returns: float
    """

    return h * L / D