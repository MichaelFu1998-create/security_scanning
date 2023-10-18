def Grigoras(Tc=None, Pc=None, Vc=None):
    r'''Relatively recent (1990) relationship for estimating critical
    properties from each other. Two of the three properties are required.
    This model uses the "critical surface", a general plot of Tc vs Pc vs Vc.
    The model used 137 organic and inorganic compounds to derive the equation.
    The general equation is in [1]_:

    .. math::
        P_c = 2.9 + 20.2 \frac{T_c}{V_c}

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
    Internal units are bar, cm^3/mol, and K. A slight error occurs when
    Pa, cm^3/mol and K are used instead, on the order of <0.2%.
    This equation is less accurate than that of Ihmels, but surprisingly close.
    The author also investigated an early QSPR model.

    Examples
    --------
    Succinic acid [110-15-6]

    >>> Grigoras(Tc=851.0, Vc=0.000308)
    5871233.766233766

    References
    ----------
    .. [1] Grigoras, Stelian. "A Structural Approach to Calculate Physical
           Properties of Pure Organic Substances: The Critical Temperature,
           Critical Volume and Related Properties." Journal of Computational
           Chemistry 11, no. 4 (May 1, 1990): 493-510.
           doi:10.1002/jcc.540110408
    '''
    if Tc and Vc:
        Vc = Vc*1E6  # m^3/mol to cm^3/mol
        Pc = 2.9 + 20.2*Tc/Vc
        Pc = Pc*1E5  # bar to Pa
        return Pc
    elif Tc and Pc:
        Pc = Pc/1E5  # Pa to bar
        Vc = 202.0*Tc/(10*Pc-29.0)
        Vc = Vc/1E6  # cm^3/mol to m^3/mol
        return Vc
    elif Pc and Vc:
        Pc = Pc/1E5  # Pa to bar
        Vc = Vc*1E6  # m^3/mol to cm^3/mol
        Tc = 1.0/202*(10*Pc-29.0)*Vc
        return Tc
    else:
        raise Exception('Two of Tc, Pc, and Vc must be provided')