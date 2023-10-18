def Stockmayer(Tm=None, Tb=None, Tc=None, Zc=None, omega=None,
               CASRN='', AvailableMethods=False, Method=None):
    r'''This function handles the retrieval or calculation a chemical's
    Stockmayer parameter. Values are available from one source with lookup
    based on CASRNs, or can be estimated from 7 CSP methods.
    Will automatically select a data source to use if no Method is provided;
    returns None if the data is not available.

    Prefered sources are 'Magalhães, Lito, Da Silva, and Silva (2013)' for
    common chemicals which had valies listed in that source, and the CSP method
    `Tee, Gotoh, and Stewart CSP with Tc, omega (1966)` for chemicals which
    don't.

    Examples
    --------
    >>> Stockmayer(CASRN='64-17-5')
    1291.41

    Parameters
    ----------
    Tm : float, optional
        Melting temperature of fluid [K]
    Tb : float, optional
        Boiling temperature of fluid [K]
    Tc : float, optional
        Critical temperature, [K]
    Zc : float, optional
        Critical compressibility, [-]
    omega : float, optional
        Acentric factor of compound, [-]
    CASRN : string, optional
        CASRN [-]

    Returns
    -------
    epsilon_k : float
        Lennard-Jones depth of potential-energy minimum over k, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain epsilon with the given
        inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Stockmayer_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        epsilon for the desired chemical, and will return methods instead of
        epsilon

    Notes
    -----
    These values are somewhat rough, as they attempt to pigeonhole a chemical
    into L-J behavior.

    The tabulated data is from [2]_, for 322 chemicals.

    References
    ----------
    .. [1] Bird, R. Byron, Warren E. Stewart, and Edwin N. Lightfoot.
       Transport Phenomena, Revised 2nd Edition. New York:
       John Wiley & Sons, Inc., 2006
    .. [2] Magalhães, Ana L., Patrícia F. Lito, Francisco A. Da Silva, and
       Carlos M. Silva. "Simple and Accurate Correlations for Diffusion
       Coefficients of Solutes in Liquids and Supercritical Fluids over Wide
       Ranges of Temperature and Density." The Journal of Supercritical Fluids
       76 (April 2013): 94-114. doi:10.1016/j.supflu.2013.02.002.
    '''
    def list_methods():
        methods = []
        if CASRN in MagalhaesLJ_data.index:
            methods.append(MAGALHAES)
        if Tc and omega:
            methods.append(TEEGOTOSTEWARD2)
        if Tc:
            methods.append(FLYNN)
            methods.append(BSLC)
            methods.append(TEEGOTOSTEWARD1)
        if Tb:
            methods.append(BSLB)
        if Tm:
            methods.append(BSLM)
        if Tc and Zc:
            methods.append(STIELTHODOS)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == FLYNN:
        epsilon = epsilon_Flynn(Tc)
    elif Method == BSLC:
        epsilon = epsilon_Bird_Stewart_Lightfoot_critical(Tc)
    elif Method == BSLB:
        epsilon = epsilon_Bird_Stewart_Lightfoot_boiling(Tb)
    elif Method == BSLM:
        epsilon = epsilon_Bird_Stewart_Lightfoot_melting(Tm)
    elif Method == STIELTHODOS:
        epsilon = epsilon_Stiel_Thodos(Tc, Zc)
    elif Method == TEEGOTOSTEWARD1:
        epsilon = epsilon_Tee_Gotoh_Steward_1(Tc)
    elif Method == TEEGOTOSTEWARD2:
        epsilon = epsilon_Tee_Gotoh_Steward_2(Tc, omega)

    elif Method == MAGALHAES:
        epsilon = float(MagalhaesLJ_data.at[CASRN, "epsilon"])
    elif Method == NONE:
        epsilon = None
    else:
        raise Exception('Failure in in function')
    return epsilon