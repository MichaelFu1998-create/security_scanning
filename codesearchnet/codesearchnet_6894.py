def Meissner(Tc=None, Pc=None, Vc=None):
    r'''Old (1942) relationship for estimating critical
    properties from each other. Two of the three properties are required.
    This model uses the "critical surface", a general plot of Tc vs Pc vs Vc.
    The model used 42 organic and inorganic compounds to derive the equation.
    The general equation is in [1]_:

    .. math::
        P_c = \frac{2.08 T_c}{V_c-8}

    Parameters
    ----------
    Tc : float, optional
        Critical temperature of fluid [K]
    Pc : float, optional
        Critical pressure of fluid [Pa]
    Vc : float, optional
        Critical volume of fluid [m^3/mol]

    Returns
    -------
    Tc, Pc or Vc : float
        Critical property of fluid [K], [Pa], or [m^3/mol]

    Notes
    -----
    The prediction of Tc from Pc and Vc is not tested, as this is not necessary
    anywhere, but it is implemented.
    Internal units are atm, cm^3/mol, and K. A slight error occurs when
    Pa, cm^3/mol and K are used instead, on the order of <0.2%.
    This equation is less accurate than that of Ihmels, but surprisingly close.
    The author also proposed means of estimated properties independently.

    Examples
    --------
    Succinic acid [110-15-6]

    >>> Meissner(Tc=851.0, Vc=0.000308)
    5978445.199999999

    References
    ----------
    .. [1] Meissner, H. P., and E. M. Redding. "Prediction of Critical
           Constants." Industrial & Engineering Chemistry 34, no. 5
           (May 1, 1942): 521-26. doi:10.1021/ie50389a003.
    '''
    if Tc and Vc:
        Vc = Vc*1E6
        Pc = 20.8*Tc/(Vc-8)
        Pc = 101325*Pc  # atm to Pa
        return Pc
    elif Tc and Pc:
        Pc = Pc/101325.  # Pa to atm
        Vc = 104/5.0*Tc/Pc+8
        Vc = Vc/1E6  # cm^3/mol to m^3/mol
        return Vc
    elif Pc and Vc:
        Pc = Pc/101325.  # Pa to atm
        Vc = Vc*1E6  # m^3/mol to cm^3/mol
        Tc = 5./104.0*Pc*(Vc-8)
        return Tc
    else:
        raise Exception('Two of Tc, Pc, and Vc must be provided')