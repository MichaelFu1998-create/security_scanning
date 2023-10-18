def Zabransky_cubic_integral(T, a1, a2, a3, a4):
    r'''Calculates the integral of liquid heat capacity using the model 
    developed in [1]_.

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a4 : float
        Coefficients

    Returns
    -------
    H : float
        Difference in enthalpy from 0 K, [J/mol]

    Notes
    -----
    The analytical integral was derived with Sympy; it is a simple polynomial.

    Examples
    --------
    >>> Zabransky_cubic_integral(298.15, 20.9634, -10.1344, 2.8253, -0.256738)
    31051.679845520586

    References
    ----------
    .. [1] Zabransky, M., V. Ruzicka Jr, V. Majer, and Eugene S. Domalski.
       Heat Capacity of Liquids: Critical Review and Recommended Values.
       2 Volume Set. Washington, D.C.: Amer Inst of Physics, 1996.
    '''
    T = T/100.
    return 100*R*T*(T*(T*(T*a4*0.25 + a3/3.) + a2*0.5) + a1)