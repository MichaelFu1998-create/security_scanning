def conductivity(CASRN=None, AvailableMethods=False, Method=None, full_info=True):
    r'''This function handles the retrieval of a chemical's conductivity.
    Lookup is based on CASRNs. Will automatically select a data source to use
    if no Method is provided; returns None if the data is not available.

    Function has data for approximately 100 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    kappa : float
        Electrical conductivity of the fluid, [S/m]
    T : float, only returned if full_info == True
        Temperature at which conductivity measurement was made
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain RI with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        conductivity_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        conductivity for the desired chemical, and will return methods instead
        of conductivity
    full_info : bool, optional
        If True, function will return the temperature at which the conductivity
        reading was made

    Notes
    -----
    Only one source is available in this function. It is:

        * 'LANGE_COND' which is from Lange's Handbook, Table 8.34 Electrical 
        Conductivity of Various Pure Liquids', a compillation of data in [1]_.

    Examples
    --------
    >>> conductivity('7732-18-5')
    (4e-06, 291.15)

    References
    ----------
    .. [1] Speight, James. Lange's Handbook of Chemistry. 16 edition.
       McGraw-Hill Professional, 2005.
    '''
    def list_methods():
        methods = []
        if CASRN in Lange_cond_pure.index:
            methods.append(LANGE_COND)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    if Method == LANGE_COND:
        kappa = float(Lange_cond_pure.at[CASRN, 'Conductivity'])
        if full_info:
            T = float(Lange_cond_pure.at[CASRN, 'T'])

    elif Method == NONE:
        kappa, T = None, None
    else:
        raise Exception('Failure in in function')

    if full_info:
        return kappa, T
    else:
        return kappa