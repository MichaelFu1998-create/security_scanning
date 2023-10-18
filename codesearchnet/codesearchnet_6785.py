def Tm(CASRN, AvailableMethods=False, Method=None, IgnoreMethods=[]):
    r'''This function handles the retrieval of a chemical's melting
    point. Lookup is based on CASRNs. Will automatically select a data
    source to use if no Method is provided; returns None if the data is not
    available.

    Prefered sources are 'Open Notebook Melting Points', with backup sources
    'CRC Physical Constants, organic' for organic chemicals, and
    'CRC Physical Constants, inorganic' for inorganic chemicals. Function has
    data for approximately 14000 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Tm : float
        Melting temperature, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Tm with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Tm_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Tm for the desired chemical, and will return methods instead of Tm
    IgnoreMethods : list, optional
        A list of methods to ignore in obtaining the full list of methods

    Notes
    -----
    A total of three sources are available for this function. They are:

        * 'OPEN_NTBKM, a compillation of data on organics
          as published in [1]_ as Open Notebook Melting Points; Averaged 
          (median) values were used when
          multiple points were available. For more information on this
          invaluable and excellent collection, see
          http://onswebservices.wikispaces.com/meltingpoint.
        * 'CRC_ORG', a compillation of data on organics
          as published in [2]_.
        * 'CRC_INORG', a compillation of data on
          inorganic as published in [2]_.

    Examples
    --------
    >>> Tm(CASRN='7732-18-5')
    273.15

    References
    ----------
    .. [1] Bradley, Jean-Claude, Antony Williams, and Andrew Lang.
       "Jean-Claude Bradley Open Melting Point Dataset", May 20, 2014.
       https://figshare.com/articles/Jean_Claude_Bradley_Open_Melting_Point_Datset/1031637.
    .. [2] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
    '''
    def list_methods():
        methods = []
        if CASRN in Tm_ON_data.index:
            methods.append(OPEN_NTBKM)
        if CASRN in CRC_inorganic_data.index and not np.isnan(CRC_inorganic_data.at[CASRN, 'Tm']):
            methods.append(CRC_INORG)
        if CASRN in CRC_organic_data.index and not np.isnan(CRC_organic_data.at[CASRN, 'Tm']):
            methods.append(CRC_ORG)
        if IgnoreMethods:
            for Method in IgnoreMethods:
                if Method in methods:
                    methods.remove(Method)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == OPEN_NTBKM:
        return float(Tm_ON_data.at[CASRN, 'Tm'])
    elif Method == CRC_INORG:
        return float(CRC_inorganic_data.at[CASRN, 'Tm'])
    elif Method == CRC_ORG:
        return float(CRC_organic_data.at[CASRN, 'Tm'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')