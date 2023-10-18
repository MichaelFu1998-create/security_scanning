def Re(L: float, v: float, nu: float) -> float:
    """
    Calculate the Reynolds number.

    :param L: [m] surface characteristic length.
    :param v: [m/s] fluid velocity relative to the object.
    :param nu: [m2/s] fluid kinematic viscosity.

    :returns: float
    """

    return v * L / nu