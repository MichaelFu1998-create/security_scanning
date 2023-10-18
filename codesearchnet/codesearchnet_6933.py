def omega_mixture(omegas, zs, CASRNs=None, Method=None,
                  AvailableMethods=False):
    r'''This function handles the calculation of a mixture's acentric factor.
    Calculation is based on the omegas provided for each pure component. Will
    automatically select a method to use if no Method is provided;
    returns None if insufficient data is available.

    Examples
    --------
    >>> omega_mixture([0.025, 0.12], [0.3, 0.7])
    0.0915

    Parameters
    ----------
    omegas : array-like
        acentric factors of each component, [-]
    zs : array-like
        mole fractions of each component, [-]
    CASRNs: list of strings
        CASRNs, not currently used [-]

    Returns
    -------
    omega : float
        acentric factor of the mixture, [-]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain omega with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        The method name to use. Only 'SIMPLE' is accepted so far.
        All valid values are also held in the list omega_mixture_methods.
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        omega for the desired chemical, and will return methods instead of
        omega

    Notes
    -----
    The only data used in the methods implemented to date are mole fractions
    and pure-component omegas. An alternate definition could be based on
    the dew point or bubble point of a multicomponent mixture, but this has
    not been done to date.

    References
    ----------
    .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    '''
    def list_methods():
        methods = []
        if none_and_length_check([zs, omegas]):
            methods.append('SIMPLE')
        methods.append('NONE')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == 'SIMPLE':
        _omega = mixing_simple(zs, omegas)
    elif Method == 'NONE':
        _omega = None
    else:
        raise Exception('Failure in in function')
    return _omega