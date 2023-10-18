def ODP(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's Ozone Depletion
    Potential, relative to CFC-11 (trichlorofluoromethane). Lookup is based on
    CASRNs. Will automatically select a data source to use if no Method is
    provided; returns None if the data is not available.

    Returns the ODP of a chemical according to [2]_ when a method is not
    specified. If a range is provided in [2]_, the highest value is returned.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    ODP : float or str
        Ozone Depletion potential, [(impact/mass chemical)/(impact/mass CFC-11)];
        if method selected has `string` in it, this will be returned as a
        string regardless of if a range is given or a number
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain ODP with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        The method name to use. Accepted methods are 'ODP2 Max', 'ODP2 Min', 
        'ODP2 string', 'ODP2 logarithmic average', and methods for older values
        are 'ODP1 Max', 'ODP1 Min', 'ODP1 string', and 'ODP1 logarithmic average'.
        All valid values are also held in the list ODP_methods.
    Method : string, optional
        A string for the method name to use, as defined by constants in
        ODP_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the ODP for the desired chemical, and will return methods
        instead of the ODP

    Notes
    -----
    Values are tabulated only for a small number of halogenated hydrocarbons,
    responsible for the largest impact. The original values of ODP as defined
    in the Montreal Protocol are also available, as methods with the `ODP1`
    prefix.

    All values are somewhat emperical, as actual reaction rates of chemicals
    with ozone depend on temperature which depends on latitude, longitude,
    time of day, weather, and the concentrations of other pollutants.

    All data is from [1]_. Several mixtures listed in [1]_ are not included
    here as they are not pure species.
    Methods for values in [2]_ are 'ODP2 Max', 'ODP2 Min', 'ODP2 string',
    'ODP2 logarithmic average',  and methods for older values are 'ODP1 Max',
    'ODP1 Min', 'ODP1 string', and 'ODP1 logarithmic average'.

    Examples
    --------
    Dichlorotetrafluoroethane, according to [2]_.

    >>> ODP(CASRN='76-14-2')
    0.58

    References
    ----------
    .. [1] US EPA, OAR. "Ozone-Depleting Substances." Accessed April 26, 2016.
       https://www.epa.gov/ozone-layer-protection/ozone-depleting-substances.
    .. [2] WMO (World Meteorological Organization), 2011: Scientific Assessment
       of Ozone Depletion: 2010. Global Ozone Research and Monitoring
       Project-Report No. 52, Geneva, Switzerland, 516 p.
       https://www.wmo.int/pages/prog/arep/gaw/ozone_2010/documents/Ozone-Assessment-2010-complete.pdf
    '''
    def list_methods():
        methods = []
        if CASRN in ODP_data.index:
            if not pd.isnull(ODP_data.at[CASRN, 'ODP2 Max']):
                methods.append(ODP2MAX)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP1 Max']):
                methods.append(ODP1MAX)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP2 Design']):
                methods.append(ODP2LOG)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP1 Design']):
                methods.append(ODP1LOG)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP2 Min']):
                methods.append(ODP2MIN)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP1 Min']):
                methods.append(ODP1MIN)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP2']):
                methods.append(ODP2STR)
            if not pd.isnull(ODP_data.at[CASRN, 'ODP1']):
                methods.append(ODP1STR)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == ODP2MAX:
        return float(ODP_data.at[CASRN, 'ODP2 Max'])
    elif Method == ODP1MAX:
        return float(ODP_data.at[CASRN, 'ODP1 Max'])
    elif Method == ODP2MIN:
        return float(ODP_data.at[CASRN, 'ODP2 Min'])
    elif Method == ODP1MIN:
        return float(ODP_data.at[CASRN, 'ODP1 Min'])
    elif Method == ODP2LOG:
        return float(ODP_data.at[CASRN, 'ODP2 Design'])
    elif Method == ODP1LOG:
        return float(ODP_data.at[CASRN, 'ODP1 Design'])
    elif Method == ODP2STR:
        return str(ODP_data.at[CASRN, 'ODP2'])
    elif Method == ODP1STR:
        return str(ODP_data.at[CASRN, 'ODP1'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')