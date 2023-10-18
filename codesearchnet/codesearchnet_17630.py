def Ra(L: float, Ts: float, Tf: float, alpha: float, beta: float, nu: float
       ) -> float:
    """
    Calculate the Ralleigh number.

    :param L: [m] heat transfer surface characteristic length.
    :param Ts: [K] heat transfer surface temperature.
    :param Tf: [K] bulk fluid temperature.
    :param alpha: [m2/s] fluid thermal diffusivity.
    :param beta: [1/K] fluid coefficient of thermal expansion.
    :param nu: [m2/s] fluid kinematic viscosity.

    :returns: float

    Ra = Gr*Pr

    Characteristic dimensions:
        * vertical plate: vertical length
        * pipe: diameter
        * bluff body: diameter
    """

    return g * beta * (Ts - Tinf) * L**3.0 / (nu * alpha)