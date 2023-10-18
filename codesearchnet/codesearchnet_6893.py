def Ihmels(Tc=None, Pc=None, Vc=None):
    r'''Most recent, and most recommended method of estimating critical
    properties from each other. Two of the three properties are required.
    This model uses the "critical surface", a general plot of Tc vs Pc vs Vc.
    The model used 421 organic compounds to derive equation.
    The general equation is in [1]_:

    .. math::
        P_c = -0.025 + 2.215 \frac{T_c}{V_c}

    Parameters
    ----------
    Tc : float
        Critical temperature of fluid (optional) [K]
    Pc : float
        Critical pressure of fluid (optional) [Pa]
    Vc : float
        Critical volume of fluid (optional) [m^3/mol]

    Returns
    -------
    Tc, Pc or Vc : float
        Critical property of fluid [K], [Pa], or [m^3/mol]

    Notes
    -----
    The prediction of Tc from Pc and Vc is not tested, as this is not necessary
    anywhere, but it is implemented.
    Internal units are MPa, cm^3/mol, and K. A slight error occurs when
    Pa, cm^3/mol and K are used instead, on the order of <0.2%.
    Their equation was also compared with 56 inorganic and elements.
    Devations of 20% for <200K or >1000K points.

    Examples
    --------a
    Succinic acid [110-15-6]

    >>> Ihmels(Tc=851.0, Vc=0.000308)
    6095016.233766234

    References
    ----------
    .. [1] Ihmels, E. Christian. "The Critical Surface." Journal of Chemical
           & Engineering Data 55, no. 9 (September 9, 2010): 3474-80.
           doi:10.1021/je100167w.
    '''
    if Tc and Vc:
        Vc = Vc*1E6  # m^3/mol to cm^3/mol
        Pc = -0.025+2.215*Tc/Vc
        Pc = Pc*1E6  # MPa to Pa
        return Pc
    elif Tc and Pc:
        Pc = Pc/1E6  # Pa to MPa
        Vc = 443*Tc/(200*Pc+5)
        Vc = Vc/1E6  # cm^3/mol to m^3/mol
        return Vc
    elif Pc and Vc:
        Pc = Pc/1E6  # Pa to MPa
        Vc = Vc*1E6  # m^3/mol to cm^3/mol
        Tc = 5.0/443*(40*Pc*Vc + Vc)
        return Tc
    else:
        raise Exception('Two of Tc, Pc, and Vc must be provided')