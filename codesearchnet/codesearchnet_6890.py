def UNIFAC_psi(T, subgroup1, subgroup2, subgroup_data, interaction_data, 
               modified=False):
    r'''Calculates the interaction parameter psi(m, n) for two UNIFAC 
    subgroups, given the system temperature, the UNIFAC subgroups considered 
    for the variant of UNIFAC used, the interaction parameters for the 
    variant of UNIFAC used, and whether or not the temperature dependence is 
    modified from the original form, as shown below.

    Original temperature dependence:
        
    .. math::
        \Psi_{mn} = \exp\left(\frac{-a_{mn}}{T}\right)
        
    Modified temperature dependence:
        
    .. math::
        \Psi_{mn} = \exp\left(\frac{-a_{mn} - b_{mn}T - c_{mn}T^2}{T}\right)
        
    Parameters
    ----------
    T : float
        Temperature of the system, [K]
    subgroup1 : int
        First UNIFAC subgroup for identifier, [-]
    subgroup2 : int
        Second UNIFAC subgroup for identifier, [-]
    subgroup_data : dict[UNIFAC_subgroup]
        Normally provided as inputs to `UNIFAC`.
    interaction_data : dict[dict[tuple(a_mn, b_mn, c_mn)]]
        Normally provided as inputs to `UNIFAC`.
    modified : bool
        True if the modified temperature dependence is used by the interaction
        parameters, otherwise False

    Returns
    -------
    psi : float
        UNIFAC interaction parameter term, [-]

    Notes
    -----
    UNIFAC interaction parameters are asymmetric. No warning is raised if an
    interaction parameter is missing.

    Examples
    --------
    >>> from thermo.unifac import UFSG, UFIP, DOUFSG, DOUFIP2006
    
    >>> UNIFAC_psi(307, 18, 1, UFSG, UFIP)
    0.9165248264184787
    
    >>> UNIFAC_psi(373.15, 9, 78, DOUFSG, DOUFIP2006, modified=True)
    1.3703140538273264
    
    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    .. [2] Fredenslund, Aage, Russell L. Jones, and John M. Prausnitz. "Group
       Contribution Estimation of Activity Coefficients in Nonideal Liquid 
       Mixtures." AIChE Journal 21, no. 6 (November 1, 1975): 1086-99. 
       doi:10.1002/aic.690210607.
    '''
    main1 = subgroup_data[subgroup1].main_group_id
    main2 = subgroup_data[subgroup2].main_group_id
    if modified:
        try:
            a, b, c = interaction_data[main1][main2]
        except:
            return 1.
        return exp((-a/T -b - c*T))
    else:
        try:
            return exp(-interaction_data[main1][main2]/T)
        except:
            return 1.