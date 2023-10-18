def Gr(L: float, Ts: float, Tf: float, beta: float, nu: float, g: float):
    """
    Calculate the Grashof number.

    :param L: [m] heat transfer surface characteristic length.
    :param Ts: [K] heat transfer surface temperature.
    :param Tf: [K] bulk fluid temperature.
    :param beta: [1/K] fluid coefficient of thermal expansion.
    :param nu: [m2/s] fluid kinematic viscosity.

    :returns: float

    .. math::
        \\mathrm{Gr} = \\frac{g \\beta (Ts - Tinf ) L^3}{\\nu ^2}

    Characteristic dimensions:
        * vertical plate: vertical length
        * pipe: diameter
        * bluff body: diameter
    """

    return g * beta * (Ts - Tf) * L**3.0 / nu**2.0