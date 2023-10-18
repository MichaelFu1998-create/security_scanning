def Zabransky_cubic_integral_over_T(T, a1, a2, a3, a4):
    r'''Calculates the integral of liquid heat capacity over T using the model 
    developed in [1]_.

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a4 : float
        Coefficients

    Returns
    -------
    S : float
        Difference in entropy from 0 K, [J/mol/K]

    Notes
    -----
    The analytical integral was derived with Sympy; it is a simple polynomial,
    plus a logarithm

    Examples
    --------
    >>> Zabransky_cubic_integral_over_T(298.15, 20.9634, -10.1344, 2.8253, 
    ... -0.256738)
    24.73245695987246

    References
    ----------
    .. [1] Zabransky, M., V. Ruzicka Jr, V. Majer, and Eugene S. Domalski.
       Heat Capacity of Liquids: Critical Review and Recommended Values.
       2 Volume Set. Washington, D.C.: Amer Inst of Physics, 1996.
    '''
    T = T/100.
    return R*(T*(T*(T*a4/3 + a3/2) + a2) + a1*log(T))