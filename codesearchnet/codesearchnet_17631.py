def Nu(L: float, h: float, k: float) -> float:
    """
    Calculate the Nusselt number.

    :param L: [m] heat transfer surface characteristic length.
    :param h: [W/K/m2] convective heat transfer coefficient.
    :param k: [W/K/m] fluid thermal conductivity.

    :returns: float
    """

    return h * L / k