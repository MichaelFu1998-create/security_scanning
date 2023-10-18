def Hf_l(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's liquid standard
    phase heat of formation. The lookup is based on CASRNs. Selects the only
    data source available, Active Thermochemical Tables (l), if the chemical is
    in it. Returns None if the data is not available.

    Function has data for 34 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Hfl : float
        Liquid standard-state heat of formation, [J/mol]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Hf(l) with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Hf_l_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Hf(l) for the desired chemical, and will return methods instead of Hf(l)

    Notes
    -----
    Only one source of information is available to this function. It is:

        * 'ATCT_L', the Active Thermochemical Tables version 1.112.

    Examples
    --------
    >>> Hf_l('67-56-1')
    -238400.0

    References
    ----------
    .. [1] Ruscic, Branko, Reinhardt E. Pinzon, Gregor von Laszewski, Deepti
       Kodeboyina, Alexander Burcat, David Leahy, David Montoy, and Albert F.
       Wagner. "Active Thermochemical Tables: Thermochemistry for the 21st
       Century." Journal of Physics: Conference Series 16, no. 1
       (January 1, 2005): 561. doi:10.1088/1742-6596/16/1/078.
    '''
    def list_methods():
        methods = []
        if CASRN in ATcT_l.index:
            methods.append(ATCT_L)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == ATCT_L:
        _Hfl = float(ATcT_l.at[CASRN, 'Hf_298K'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')
    return _Hfl