def EQ105(T, A, B, C, D):
    r'''DIPPR Equation #105. Often used in calculating liquid molar density.
    All 4 parameters are required. C is sometimes the fluid's critical
    temperature.

    .. math::
        Y = \frac{A}{B^{1 + (1-\frac{T}{C})^D}}

    Parameters
    ----------
    T : float
        Temperature, [K]
    A-D : float
        Parameter for the equation; chemical and property specific [-]

    Returns
    -------
    Y : float
        Property [constant-specific]
        
    Notes
    -----
    This expression can be integrated in terms of the incomplete gamma function
    for dT, but for Y/T dT no integral could be found.

    Examples
    --------
    Hexane molar density; DIPPR coefficients normally in kmol/m^3.

    >>> EQ105(300., 0.70824, 0.26411, 507.6, 0.27537)
    7.593170096339236

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    return A/B**(1. + (1. - T/C)**D)