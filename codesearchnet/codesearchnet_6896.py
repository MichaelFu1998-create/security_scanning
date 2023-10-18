def critical_surface(Tc=None, Pc=None, Vc=None, AvailableMethods=False,
                     Method=None):
    r'''Function for calculating a critical property of a substance from its
    other two critical properties. Calls functions Ihmels, Meissner, and
    Grigoras, each of which use a general 'Critical surface' type of equation.
    Limited accuracy is expected due to very limited theoretical backing.

    Parameters
    ----------
    Tc : float
        Critical temperature of fluid (optional) [K]
    Pc : float
        Critical pressure of fluid (optional) [Pa]
    Vc : float
        Critical volume of fluid (optional) [m^3/mol]
    AvailableMethods : bool
        Request available methods for given parameters
    Method : string
        Request calculation uses the requested method

    Returns
    -------
    Tc, Pc or Vc : float
        Critical property of fluid [K], [Pa], or [m^3/mol]

    Notes
    -----

    Examples
    --------
    Decamethyltetrasiloxane [141-62-8]

    >>> critical_surface(Tc=599.4, Pc=1.19E6, Method='IHMELS')
    0.0010927333333333334
    '''
    def list_methods():
        methods = []
        if (Tc and Pc) or (Tc and Vc) or (Pc and Vc):
            methods.append(IHMELS)
            methods.append(MEISSNER)
            methods.append(GRIGORAS)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == IHMELS:
        Third = Ihmels(Tc=Tc, Pc=Pc, Vc=Vc)
    elif Method == MEISSNER:
        Third = Meissner(Tc=Tc, Pc=Pc, Vc=Vc)
    elif Method == GRIGORAS:
        Third = Grigoras(Tc=Tc, Pc=Pc, Vc=Vc)
    elif Method == NONE:
        Third = None
    else:
        raise Exception('Failure in in function')
    return Third