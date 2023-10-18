def Zabransky_quasi_polynomial_integral(T, Tc, a1, a2, a3, a4, a5, a6):
    r'''Calculates the integral of liquid heat capacity using the  
    quasi-polynomial model developed in [1]_.

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a6 : float
        Coefficients

    Returns
    -------
    H : float
        Difference in enthalpy from 0 K, [J/mol]

    Notes
    -----
    The analytical integral was derived with SymPy; it is a simple polynomial
    plus some logarithms.

    Examples
    --------
    >>> H2 = Zabransky_quasi_polynomial_integral(300, 591.79, -3.12743, 
    ... 0.0857315, 13.7282, 1.28971, 6.42297, 4.10989)
    >>> H1 = Zabransky_quasi_polynomial_integral(200, 591.79, -3.12743, 
    ... 0.0857315, 13.7282, 1.28971, 6.42297, 4.10989)
    >>> H2 - H1
    14662.026406892925

    References
    ----------
    .. [1] Zabransky, M., V. Ruzicka Jr, V. Majer, and Eugene S. Domalski.
       Heat Capacity of Liquids: Critical Review and Recommended Values.
       2 Volume Set. Washington, D.C.: Amer Inst of Physics, 1996.
    '''
    Tc2 = Tc*Tc
    Tc3 = Tc2*Tc
    term = T - Tc
    return R*(T*(T*(T*(T*a6/(4.*Tc3) + a5/(3.*Tc2)) + a4/(2.*Tc)) - a1 + a3) 
              + T*a1*log(1. - T/Tc) - 0.5*Tc*(a1 + a2)*log(term*term))