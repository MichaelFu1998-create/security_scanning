def molecular_diameter(Tc=None, Pc=None, Vc=None, Zc=None, omega=None,
          Vm=None, Vb=None, CASRN='', AvailableMethods=False, Method=None):
    r'''This function handles the retrieval or calculation a chemical's
    L-J molecular diameter. Values are available from one source with lookup
    based on CASRNs, or can be estimated from 9 CSP methods.
    Will automatically select a data source to use if no Method is provided;
    returns None if the data is not available.

    Prefered sources are 'Magalhães, Lito, Da Silva, and Silva (2013)' for
    common chemicals which had valies listed in that source, and the CSP method
    `Tee, Gotoh, and Stewart CSP with Tc, Pc, omega (1966)` for chemicals which
    don't.

    Examples
    --------
    >>> molecular_diameter(CASRN='64-17-5')
    4.23738

    Parameters
    ----------
    Tc : float, optional
        Critical temperature, [K]
    Pc : float, optional
        Critical pressure, [Pa]
    Vc : float, optional
        Critical volume, [m^3/mol]
    Zc : float, optional
        Critical compressibility, [-]
    omega : float, optional
        Acentric factor of compound, [-]
    Vm : float, optional
        Molar volume of liquid at the melting point of the fluid [K]
    Vb : float, optional
        Molar volume of liquid at the boiling point of the fluid [K]
    CASRN : string, optional
        CASRN [-]

    Returns
    -------
    sigma : float
        Lennard-Jones molecular diameter, [Angstrom]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain epsilon with the given
        inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        molecular_diameter_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        sigma for the desired chemical, and will return methods instead of
        sigma

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
        if Tc and Pc and omega:
            methods.append(TEEGOTOSTEWARD4)
        if Tc and Pc:
            methods.append(SILVALIUMACEDO)
            methods.append(BSLC2)
            methods.append(TEEGOTOSTEWARD3)
        if Vc and Zc:
            methods.append(STIELTHODOSMD)
        if Vc:
            methods.append(FLYNN)
            methods.append(BSLC1)
        if Vb:
            methods.append(BSLB)
        if Vm:
            methods.append(BSLM)
        methods.append(NONE)
        return methods

    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    if Method == FLYNN:
        sigma = sigma_Flynn(Vc)
    elif Method == BSLC1:
        sigma = sigma_Bird_Stewart_Lightfoot_critical_1(Vc)
    elif Method == BSLC2:
        sigma = sigma_Bird_Stewart_Lightfoot_critical_2(Tc, Pc)
    elif Method == TEEGOTOSTEWARD3:
        sigma = sigma_Tee_Gotoh_Steward_1(Tc, Pc)
    elif Method == SILVALIUMACEDO:
        sigma = sigma_Silva_Liu_Macedo(Tc, Pc)
    elif Method == BSLB:
        sigma = sigma_Bird_Stewart_Lightfoot_boiling(Vb)
    elif Method == BSLM:
        sigma = sigma_Bird_Stewart_Lightfoot_melting(Vm)
    elif Method == STIELTHODOSMD:
        sigma = sigma_Stiel_Thodos(Vc, Zc)
    elif Method == TEEGOTOSTEWARD4:
        sigma = sigma_Tee_Gotoh_Steward_2(Tc, Pc, omega)
    elif Method == MAGALHAES:
        sigma = float(MagalhaesLJ_data.at[CASRN, "sigma"])
    elif Method == NONE:
        sigma = None
    else:
        raise Exception('Failure in in function')
    return sigma