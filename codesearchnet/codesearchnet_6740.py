def TRC_Antoine_extended(T, Tc, to, A, B, C, n, E, F):
    r'''Calculates vapor pressure of a chemical using the TRC Extended Antoine
    equation. Parameters are chemical dependent, and said to be from the 
    Thermodynamics Research Center (TRC) at Texas A&M. Coefficients for various
    chemicals can be found in [1]_.

    .. math::
        \log_{10} P^{sat} = A - \frac{B}{T + C} + 0.43429x^n + Ex^8 + Fx^{12}
        
        x = \max \left(\frac{T-t_o-273.15}{T_c}, 0 \right)

    Parameters
    ----------
    T : float
        Temperature of fluid, [K]
    A, B, C, n, E, F : floats
        Regressed coefficients for the Antoine Extended (TRC) equation,
        specific for each chemical, [-]

    Returns
    -------
    Psat : float
        Vapor pressure calculated with coefficients [Pa]
    
    Notes
    -----
    Assumes coefficients are for calculating vapor pressure in Pascal. 
    Coefficients should be consistent with input temperatures in Kelvin;

    Examples
    --------
    Tetrafluoromethane, coefficients from [1]_, at 180 K:
    
    >>> TRC_Antoine_extended(180.0, 227.51, -120., 8.95894, 510.595, -15.95, 
    ... 2.41377, -93.74, 7425.9) 
    706317.0898414153

    References
    ----------
    .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    '''
    x = max((T - to - 273.15)/Tc, 0.)
    return 10.**(A - B/(T+C) + 0.43429*x**n + E*x**8 + F*x**12)