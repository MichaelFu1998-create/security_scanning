def Tt(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's triple temperature.
    Lookup is based on CASRNs. Will automatically select a data source to use
    if no Method is provided; returns None if the data is not available.

    Returns data from [1]_, or a chemical's melting point if available.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Tt : float
        Triple point temperature, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Tt with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Tt_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the Tt for the desired chemical, and will return methods
        instead of the Tt

    Notes
    -----
    Median difference between melting points and triple points is 0.02 K.
    Accordingly, this should be more than good enough for engineering
    applications.

    Temperatures are on the ITS-68 scale.

    Examples
    --------
    Ammonia

    >>> Tt('7664-41-7')
    195.47999999999999

    References
    ----------
    .. [1] Staveley, L. A. K., L. Q. Lobo, and J. C. G. Calado. "Triple-Points
       of Low Melting Substances and Their Use in Cryogenic Work." Cryogenics
       21, no. 3 (March 1981): 131-144. doi:10.1016/0011-2275(81)90264-2.
    '''
    def list_methods():
        methods = []
        if CASRN in Staveley_data.index:
            methods.append(STAVELEY)
        if Tm(CASRN):
            methods.append(MELTING)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == STAVELEY:
        Tt = Staveley_data.at[CASRN, "Tt68"]
    elif Method == MELTING:
        Tt = Tm(CASRN)
    elif Method == NONE:
        Tt = None
    else:
        raise Exception('Failure in in function')
    return Tt