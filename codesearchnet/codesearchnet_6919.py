def EQ115(T, A, B, C=0, D=0, E=0):
    r'''DIPPR Equation #115. No major uses; has been used as an alternate
    liquid viscosity expression, and as a model for vapor pressure.
    Only parameters A and B are required.

    .. math::
        Y = \exp\left(A + \frac{B}{T} + C\log T + D T^2 + \frac{E}{T^2}\right)

    Parameters
    ----------
    T : float
        Temperature, [K]
    A-E : float
        Parameter for the equation; chemical and property specific [-]

    Returns
    -------
    Y : float
        Property [constant-specific]

    Notes
    -----
    No coefficients found for this expression.
    This function is not integrable for either dT or Y/T dT.

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    return exp(A+B/T+C*log(T)+D*T**2 + E/T**2)