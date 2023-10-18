def third_property(CASRN=None, T=False, P=False, V=False):
    r'''Function for calculating a critical property of a substance from its
    other two critical properties, but retrieving the actual other critical
    values for convenient calculation.
    Calls functions Ihmels, Meissner, and
    Grigoras, each of which use a general 'Critical surface' type of equation.
    Limited accuracy is expected due to very limited theoretical backing.

    Parameters
    ----------
    CASRN : string
        The CAS number of the desired chemical
    T : bool
        Estimate critical temperature
    P : bool
        Estimate critical pressure
    V : bool
        Estimate critical volume

    Returns
    -------
    Tc, Pc or Vc : float
        Critical property of fluid [K], [Pa], or [m^3/mol]

    Notes
    -----
    Avoids recursion only by eliminating the None and critical surface options
    for calculating each critical property. So long as it never calls itself.
    Note that when used by Tc, Pc or Vc, this function results in said function
    calling the other functions (to determine methods) and (with method specified)

    Examples
    --------
    >>> # Decamethyltetrasiloxane [141-62-8]
    >>> third_property('141-62-8', V=True)
    0.0010920041152263375

    >>> # Succinic acid 110-15-6
    >>> third_property('110-15-6', P=True)
    6095016.233766234
    '''
    Third = None
    if V:
        Tc_methods = Tc(CASRN, AvailableMethods=True)[0:-2]
        Pc_methods = Pc(CASRN, AvailableMethods=True)[0:-2]
        if Tc_methods and Pc_methods:
            _Tc = Tc(CASRN=CASRN, Method=Tc_methods[0])
            _Pc = Pc(CASRN=CASRN, Method=Pc_methods[0])
            Third = critical_surface(Tc=_Tc, Pc=_Pc, Vc=None)
    elif P:
        Tc_methods = Tc(CASRN, AvailableMethods=True)[0:-2]
        Vc_methods = Vc(CASRN, AvailableMethods=True)[0:-2]
        if Tc_methods and Vc_methods:
            _Tc = Tc(CASRN=CASRN, Method=Tc_methods[0])
            _Vc = Vc(CASRN=CASRN, Method=Vc_methods[0])
            Third = critical_surface(Tc=_Tc, Vc=_Vc, Pc=None)
    elif T:
        Pc_methods = Pc(CASRN, AvailableMethods=True)[0:-2]
        Vc_methods = Vc(CASRN, AvailableMethods=True)[0:-2]
        if Pc_methods and Vc_methods:
            _Pc = Pc(CASRN=CASRN, Method=Pc_methods[0])
            _Vc = Vc(CASRN=CASRN, Method=Vc_methods[0])
            Third = critical_surface(Pc=_Pc, Vc=_Vc, Tc=None)
    else:
        raise Exception('Error in function')
    if not Third:
        return None
    return Third