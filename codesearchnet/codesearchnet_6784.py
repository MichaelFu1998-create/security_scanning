def Tb(CASRN, AvailableMethods=False, Method=None, IgnoreMethods=[PSAT_DEFINITION]):
    r'''This function handles the retrieval of a chemical's boiling
    point. Lookup is based on CASRNs. Will automatically select a data
    source to use if no Method is provided; returns None if the data is not
    available.

    Prefered sources are 'CRC Physical Constants, organic' for organic
    chemicals, and 'CRC Physical Constants, inorganic' for inorganic
    chemicals. Function has data for approximately 13000 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Tb : float
        Boiling temperature, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Tb with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Tb_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Tb for the desired chemical, and will return methods instead of Tb
    IgnoreMethods : list, optional
        A list of methods to ignore in obtaining the full list of methods,
        useful for for performance reasons and ignoring inaccurate methods

    Notes
    -----
    A total of four methods are available for this function. They are:

        * 'CRC_ORG', a compillation of data on organics
          as published in [1]_.
        * 'CRC_INORG', a compillation of data on
          inorganic as published in [1]_.
        * 'YAWS', a large compillation of data from a
          variety of sources; no data points are sourced in the work of [2]_.
        * 'PSAT_DEFINITION', calculation of boiling point from a
          vapor pressure calculation. This is normally off by a fraction of a
          degree even in the best cases. Listed in IgnoreMethods by default
          for performance reasons.

    Examples
    --------
    >>> Tb('7732-18-5')
    373.124

    References
    ----------
    .. [1] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
    .. [2] Yaws, Carl L. Thermophysical Properties of Chemicals and
       Hydrocarbons, Second Edition. Amsterdam Boston: Gulf Professional
       Publishing, 2014.
    '''
    def list_methods():
        methods = []
        if CASRN in CRC_inorganic_data.index and not np.isnan(CRC_inorganic_data.at[CASRN, 'Tb']):
            methods.append(CRC_INORG)
        if CASRN in CRC_organic_data.index and not np.isnan(CRC_organic_data.at[CASRN, 'Tb']):
            methods.append(CRC_ORG)
        if CASRN in Yaws_data.index:
            methods.append(YAWS)
        if PSAT_DEFINITION not in IgnoreMethods:
            try:
                # For some chemicals, vapor pressure range will exclude Tb
                VaporPressure(CASRN=CASRN).solve_prop(101325.)
                methods.append(PSAT_DEFINITION)
            except:  # pragma: no cover
                pass
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

    if Method == CRC_INORG:
        return float(CRC_inorganic_data.at[CASRN, 'Tb'])
    elif Method == CRC_ORG:
        return float(CRC_organic_data.at[CASRN, 'Tb'])
    elif Method == YAWS:
        return float(Yaws_data.at[CASRN, 'Tb'])
    elif Method == PSAT_DEFINITION:
        return VaporPressure(CASRN=CASRN).solve_prop(101325.)
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')