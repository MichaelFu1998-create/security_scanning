def Tautoignition(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval or calculation of a chemical's
    autoifnition temperature. Lookup is based on CASRNs. No predictive methods
    are currently implemented. Will automatically select a data source to use
    if no Method is provided; returns None if the data is not available.

    Prefered source is 'IEC 60079-20-1 (2010)' [1]_, with the secondary source
    'NFPA 497 (2008)' [2]_ having very similar data.

    Examples
    --------
    >>> Tautoignition(CASRN='71-43-2')
    771.15

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Tautoignition : float
        Autoignition point of the chemical, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Tautoignition with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Tautoignition_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Tautoignition for the desired chemical, and will return methods
        instead of Tautoignition

    Notes
    -----

    References
    ----------
    .. [1] IEC. “IEC 60079-20-1:2010 Explosive atmospheres - Part 20-1:
       Material characteristics for gas and vapour classification - Test
       methods and data.” https://webstore.iec.ch/publication/635. See also
       https://law.resource.org/pub/in/bis/S05/is.iec.60079.20.1.2010.pdf
    .. [2] National Fire Protection Association. NFPA 497: Recommended
       Practice for the Classification of Flammable Liquids, Gases, or Vapors
       and of Hazardous. NFPA, 2008.
    '''
    def list_methods():
        methods = []
        if CASRN in IEC_2010.index and not np.isnan(IEC_2010.at[CASRN, 'Tautoignition']):
            methods.append(IEC)
        if CASRN in NFPA_2008.index and not np.isnan(NFPA_2008.at[CASRN, 'Tautoignition']):
            methods.append(NFPA)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == IEC:
        return float(IEC_2010.at[CASRN, 'Tautoignition'])
    elif Method == NFPA:
        return float(NFPA_2008.at[CASRN, 'Tautoignition'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')