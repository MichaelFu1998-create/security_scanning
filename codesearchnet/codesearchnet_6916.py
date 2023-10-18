def EQ106(T, Tc, A, B, C=0, D=0, E=0):
    r'''DIPPR Equation #106. Often used in calculating liquid surface tension,
    and heat of vaporization.
    Only parameters A and B parameters are required; many fits include no
    further parameters. Critical temperature is also required.

    .. math::
        Y = A(1-T_r)^{B + C T_r + D T_r^2 + E T_r^3}

        Tr = \frac{T}{Tc}

    Parameters
    ----------
    T : float
        Temperature, [K]
    Tc : float
        Critical temperature, [K]
    A-D : float
        Parameter for the equation; chemical and property specific [-]

    Returns
    -------
    Y : float
        Property [constant-specific]

    Notes
    -----
    The integral could not be found, but the integral over T actually could,
    again in terms of hypergeometric functions.

    Examples
    --------
    Water surface tension; DIPPR coefficients normally in Pa*s.

    >>> EQ106(300, 647.096, 0.17766, 2.567, -3.3377, 1.9699)
    0.07231499373541

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    Tr = T/Tc
    return A*(1. - Tr)**(B + Tr*(C + Tr*(D + E*Tr)))