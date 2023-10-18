def GWP(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's Global Warming
    Potential, relative to CO2. Lookup is based on CASRNs. Will automatically
    select a data source to use if no Method is provided; returns None if the
    data is not available.

    Returns the GWP for the 100yr outlook by default.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    GWP : float
        Global warming potential, [(impact/mass chemical)/(impact/mass CO2)]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain GWP with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        The method name to use. Accepted methods are IPCC (2007) 100yr',
        'IPCC (2007) 100yr-SAR', 'IPCC (2007) 20yr', and 'IPCC (2007) 500yr'. 
        All valid values are also held in the list GWP_methods.
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the GWP for the desired chemical, and will return methods
        instead of the GWP

    Notes
    -----
    All data is from [1]_, the official source. Several chemicals are available
    in [1]_ are not included here as they do not have a CAS.
    Methods are 'IPCC (2007) 100yr', 'IPCC (2007) 100yr-SAR',
    'IPCC (2007) 20yr', and 'IPCC (2007) 500yr'.

    Examples
    --------
    Methane, 100-yr outlook

    >>> GWP(CASRN='74-82-8')
    25.0

    References
    ----------
    .. [1] IPCC. "2.10.2 Direct Global Warming Potentials - AR4 WGI Chapter 2:
       Changes in Atmospheric Constituents and in Radiative Forcing." 2007.
       https://www.ipcc.ch/publications_and_data/ar4/wg1/en/ch2s2-10-2.html.
    '''
    def list_methods():
        methods = []
        if CASRN in GWP_data.index:
            methods.append(IPCC100)
            if not pd.isnull(GWP_data.at[CASRN, 'SAR 100yr']):
                methods.append(IPCC100SAR)
            methods.append(IPCC20)
            methods.append(IPCC500)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == IPCC100:
        return float(GWP_data.at[CASRN, '100yr GWP'])
    elif Method == IPCC100SAR:
        return float(GWP_data.at[CASRN, 'SAR 100yr'])
    elif Method == IPCC20:
        return float(GWP_data.at[CASRN, '20yr GWP'])
    elif Method == IPCC500:
        return float(GWP_data.at[CASRN, '500yr GWP'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')