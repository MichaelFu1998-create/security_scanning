def Missenard(T, P, Tc, Pc, kl):
    r'''Adjustes for pressure the thermal conductivity of a liquid using an
    emperical formula based on [1]_, but as given in [2]_.

    .. math::
        \frac{k}{k^*} = 1 + Q P_r^{0.7}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    P : float
        Pressure of fluid [Pa]
    Tc: float
        Critical point of fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    kl : float
        Thermal conductivity of liquid at 1 atm or saturation, [W/m/K]

    Returns
    -------
    kl_dense : float
        Thermal conductivity of liquid at P, [W/m/K]

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    An interpolation routine is used here from tabulated values of Q.
    The original source has not been reviewed.

    Examples
    --------
    Example from [2]_, toluene; matches.

    >>> Missenard(304., 6330E5, 591.8, 41E5, 0.129)
    0.2198375777069657

    References
    ----------
    .. [1] Missenard, F. A., Thermal Conductivity of Organic Liquids of a
       Series or a Group of Liquids , Rev. Gen.Thermodyn., 101 649 (1970).
    .. [2] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    '''
    Tr = T/Tc
    Pr = P/Pc
    Q = float(Qfunc_Missenard(Pr, Tr))
    return kl*(1. + Q*Pr**0.7)