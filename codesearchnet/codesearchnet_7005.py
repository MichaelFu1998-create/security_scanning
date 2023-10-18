def Pt(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's triple pressure.
    Lookup is based on CASRNs. Will automatically select a data source to use
    if no Method is provided; returns None if the data is not available.

    Returns data from [1]_, or attempts to calculate the vapor pressure at the
    triple temperature, if data is available.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Pt : float
        Triple point pressure, [Pa]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Pt with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Pt_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the Pt for the desired chemical, and will return methods
        instead of the Pt

    Notes
    -----

    Examples
    --------
    Ammonia

    >>> Pt('7664-41-7')
    6079.5

    References
    ----------
    .. [1] Staveley, L. A. K., L. Q. Lobo, and J. C. G. Calado. "Triple-Points
       of Low Melting Substances and Their Use in Cryogenic Work." Cryogenics
       21, no. 3 (March 1981): 131-144. doi:10.1016/0011-2275(81)90264-2.
    '''
    def list_methods():
        methods = []
        if CASRN in Staveley_data.index and not np.isnan(Staveley_data.at[CASRN, 'Pt']):
            methods.append(STAVELEY)
        if Tt(CASRN) and VaporPressure(CASRN=CASRN).T_dependent_property(T=Tt(CASRN)):
            methods.append(DEFINITION)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == STAVELEY:
        Pt = Staveley_data.at[CASRN, 'Pt']
    elif Method == DEFINITION:
        Pt = VaporPressure(CASRN=CASRN).T_dependent_property(T=Tt(CASRN))
    elif Method == NONE:
        Pt = None
    else:
        raise Exception('Failure in in function')
    return Pt