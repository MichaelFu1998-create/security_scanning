def Hf(CASRN, AvailableMethods=False, Method=None):
    r'''This function handles the retrieval of a chemical's standard-phase
    heat of formation. The lookup is based on CASRNs. Selects the only
    data source available ('API TDB') if the chemical is in it.
    Returns None if the data is not available.

    Function has data for 571 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Hf : float
        Standard-state heat of formation, [J/mol]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Hf with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Hf_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Hf for the desired chemical, and will return methods instead of Hf

    Notes
    -----
    Only one source of information is available to this function. it is:

        * 'API_TDB', a compilation of heats of formation of unspecified phase.
          Not the original data, but as reproduced in [1]_. Some chemicals with
          duplicated CAS numbers were removed.

    Examples
    --------
    >>> Hf(CASRN='7732-18-5')
    -241820.0

    References
    ----------
    .. [1] Albahri, Tareq A., and Abdulla F. Aljasmi. "SGC Method for
       Predicting the Standard Enthalpy of Formation of Pure Compounds from
       Their Molecular Structures." Thermochimica Acta 568
       (September 20, 2013): 46-60. doi:10.1016/j.tca.2013.06.020.
    '''
    def list_methods():
        methods = []
        if CASRN in API_TDB_data.index:
            methods.append(API_TDB)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == API_TDB:
        _Hf = float(API_TDB_data.at[CASRN, 'Hf'])
    elif Method == NONE:
        _Hf = None
    else:
        raise Exception('Failure in in function')
    return _Hf