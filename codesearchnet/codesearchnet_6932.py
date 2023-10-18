def LK_omega(Tb, Tc, Pc):
    r'''Estimates the acentric factor of a fluid using a correlation in [1]_.

    .. math::
        \omega = \frac{\ln P_{br}^{sat} - 5.92714 + 6.09648/T_{br} + 1.28862
        \ln T_{br} -0.169347T_{br}^6}
        {15.2518 - 15.6875/T_{br} - 13.4721 \ln T_{br} + 0.43577 T_{br}^6}

    Parameters
    ----------
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]

    Returns
    -------
    omega : float
        Acentric factor of the fluid [-]

    Notes
    -----
    Internal units are atmosphere and Kelvin.
    Example value from Reid (1987). Using ASPEN V8.4, LK method gives 0.325595.

    Examples
    --------
    Isopropylbenzene

    >>> LK_omega(425.6, 631.1, 32.1E5)
    0.32544249926397856

    References
    ----------
    .. [1] Lee, Byung Ik, and Michael G. Kesler. "A Generalized Thermodynamic
       Correlation Based on Three-Parameter Corresponding States." AIChE Journal
       21, no. 3 (1975): 510-527. doi:10.1002/aic.690210313.
    '''
    T_br = Tb/Tc
    omega = (log(101325.0/Pc) - 5.92714 + 6.09648/T_br + 1.28862*log(T_br) -
             0.169347*T_br**6)/(15.2518 - 15.6875/T_br - 13.4721*log(T_br) +
             0.43577*T_br**6)
    return omega