def Wagner_original(T, Tc, Pc, a, b, c, d):
    r'''Calculates vapor pressure using the Wagner equation (3, 6 form).

    Requires critical temperature and pressure as well as four coefficients
    specific to each chemical.

    .. math::
        \ln P^{sat}= \ln P_c + \frac{a\tau + b \tau^{1.5} + c\tau^3 + d\tau^6}
        {T_r}
        
        \tau = 1 - \frac{T}{T_c}

    Parameters
    ----------
    T : float
        Temperature of fluid, [K]
    Tc : float
        Critical temperature, [K]
    Pc : float
        Critical pressure, [Pa]
    a, b, c, d : floats
        Parameters for wagner equation. Specific to each chemical. [-]

    Returns
    -------
    Psat : float
        Vapor pressure at T [Pa]

    Notes
    -----
    Warning: Pc is often treated as adjustable constant.

    Examples
    --------
    Methane, coefficients from [2]_, at 100 K.

    >>> Wagner_original(100.0, 190.53, 4596420., a=-6.00435, b=1.1885, 
    ... c=-0.834082, d=-1.22833)
    34520.44601450496

    References
    ----------
    .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    .. [2] McGarry, Jack. "Correlation and Prediction of the Vapor Pressures of
       Pure Liquids over Large Pressure Ranges." Industrial & Engineering
       Chemistry Process Design and Development 22, no. 2 (April 1, 1983):
       313-22. doi:10.1021/i200021a023.
    '''
    Tr = T/Tc
    tau = 1.0 - Tr
    return Pc*exp((a*tau + b*tau**1.5 + c*tau**3 + d*tau**6)/Tr)