def logP(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's octanol-water
    partition coefficient. Lookup is based on CASRNs. Will automatically
    select a data source to use if no Method is provided; returns None if the
    data is not available.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    logP : float
        Octanol-water partition coefficient, [-]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain logP with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        The method name to use. Accepted methods are 'SYRRES', or 'CRC', 
        All valid values are also held in the list logP_methods.
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the logP for the desired chemical, and will return methods
        instead of the logP

    Notes
    -----
    .. math::
        \log P_{ oct/wat} = \log\left(\frac{\left[{solute}
        \right]_{ octanol}^{un-ionized}}{\left[{solute}
        \right]_{ water}^{ un-ionized}}\right)

    Examples
    --------
    >>> logP('67-56-1')
    -0.74

    References
    ----------
    .. [1] Syrres. 2006. KOWWIN Data, SrcKowData2.zip.
       http://esc.syrres.com/interkow/Download/SrcKowData2.zip
    .. [2] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
    '''
    def list_methods():
        methods = []
        if CASRN in CRClogPDict.index:
            methods.append(CRC)
        if CASRN in SyrresDict2.index:
            methods.append(SYRRES)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == CRC:
        return float(CRClogPDict.at[CASRN, 'logP'])
    elif Method == SYRRES:
        return float(SyrresDict2.at[CASRN, 'logP'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')