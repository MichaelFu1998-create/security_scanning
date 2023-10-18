def Edalat(T, Tc, Pc, omega):
    r'''Calculates vapor pressure of a fluid at arbitrary temperatures using a
    CSP relationship by [1]_. Requires a chemical's critical temperature,
    pressure, and acentric factor. Claimed to have a higher accuracy than the
    Lee-Kesler CSP relationship.

    The vapor pressure of a chemical at `T` is given by:

    .. math::
        \ln(P^{sat}/P_c) = \frac{a\tau + b\tau^{1.5} + c\tau^3 + d\tau^6}
        {1-\tau}
        
        a = -6.1559 - 4.0855\omega
        
        b = 1.5737 - 1.0540\omega - 4.4365\times 10^{-3} d
        
        c = -0.8747 - 7.8874\omega
        
        d = \frac{1}{-0.4893 - 0.9912\omega + 3.1551\omega^2}
        
        \tau = 1 - \frac{T}{T_c}
        
    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    omega : float
        Acentric factor [-]

    Returns
    -------
    Psat : float
        Vapor pressure, [Pa]

    Notes
    -----
    [1]_ found an average error of 6.06% on 94 compounds and 1106 data points.
    
    Examples
    --------
    >>> Edalat(347.2, 617.1, 36E5, 0.299)
    13461.273080743307

    References
    ----------
    .. [1] Edalat, M., R. B. Bozar-Jomehri, and G. A. Mansoori. "Generalized 
       Equation Predicts Vapor Pressure of Hydrocarbons." Oil and Gas Journal; 
       91:5 (February 1, 1993).
    '''
    tau = 1. - T/Tc
    a = -6.1559 - 4.0855*omega
    c = -0.8747 - 7.8874*omega
    d = 1./(-0.4893 - 0.9912*omega + 3.1551*omega**2)
    b = 1.5737 - 1.0540*omega - 4.4365E-3*d
    lnPr = (a*tau + b*tau**1.5 + c*tau**3 + d*tau**6)/(1.-tau)
    return exp(lnPr)*Pc