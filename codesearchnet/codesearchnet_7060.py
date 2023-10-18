def refractive_index(CASRN, T=None, AvailableMethods=False, Method=None,
                     full_info=True):
    r'''This function handles the retrieval of a chemical's refractive
    index. Lookup is based on CASRNs. Will automatically select a data source
    to use if no Method is provided; returns None if the data is not available.

    Function has data for approximately 4500 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    RI : float
        Refractive Index on the Na D line, [-]
    T : float, only returned if full_info == True
        Temperature at which refractive index reading was made
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain RI with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        RI_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        RI for the desired chemical, and will return methods instead of RI
    full_info : bool, optional
        If True, function will return the temperature at which the refractive
        index reading was made

    Notes
    -----
    Only one source is available in this function. It is:

        * 'CRC', a compillation of Organic RI data in [1]_.

    Examples
    --------
    >>> refractive_index(CASRN='64-17-5')
    (1.3611, 293.15)

    References
    ----------
    .. [1] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
    '''
    def list_methods():
        methods = []
        if CASRN in CRC_RI_organic.index:
            methods.append(CRC)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == CRC:
        _RI = float(CRC_RI_organic.at[CASRN, 'RI'])
        if full_info:
            _T = float(CRC_RI_organic.at[CASRN, 'RIT'])
    elif Method == NONE:
        _RI, _T = None, None
    else:
        raise Exception('Failure in in function')
    if full_info:
        return _RI, _T
    else:
        return _RI