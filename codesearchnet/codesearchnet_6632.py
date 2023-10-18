def Zabransky_quasi_polynomial_integral_over_T(T, Tc, a1, a2, a3, a4, a5, a6):
    r'''Calculates the integral of liquid heat capacity over T using the 
    quasi-polynomial model  developed in [1]_.

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a6 : float
        Coefficients

    Returns
    -------
    S : float
        Difference in entropy from 0 K, [J/mol/K]

    Notes
    -----
    The analytical integral was derived with Sympy. It requires the 
    Polylog(2,x) function, which is unimplemented in SciPy. A very accurate 
    numerical approximation was implemented as :obj:`thermo.utils.polylog2`.
    Relatively slow due to the use of that special function.

    Examples
    --------
    >>> S2 = Zabransky_quasi_polynomial_integral_over_T(300, 591.79, -3.12743, 
    ... 0.0857315, 13.7282, 1.28971, 6.42297, 4.10989)
    >>> S1 = Zabransky_quasi_polynomial_integral_over_T(200, 591.79, -3.12743, 
    ... 0.0857315, 13.7282, 1.28971, 6.42297, 4.10989)
    >>> S2 - S1
    59.16997291893654
    
    References
    ----------
    .. [1] Zabransky, M., V. Ruzicka Jr, V. Majer, and Eugene S. Domalski.
       Heat Capacity of Liquids: Critical Review and Recommended Values.
       2 Volume Set. Washington, D.C.: Amer Inst of Physics, 1996.
    '''
    term = T - Tc
    logT = log(T)
    Tc2 = Tc*Tc
    Tc3 = Tc2*Tc
    return R*(a3*logT -a1*polylog2(T/Tc) - a2*(-logT + 0.5*log(term*term))
              + T*(T*(T*a6/(3.*Tc3) + a5/(2.*Tc2)) + a4/Tc))