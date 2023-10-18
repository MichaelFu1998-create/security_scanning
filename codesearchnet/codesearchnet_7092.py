def stiel_thodos_dense(T, MW, Tc, Pc, Vc, Zc, Vm, kg):
    r'''Estimates the thermal conductivity of a gas at high pressure as a
    function of temperature using difference method of Stiel and Thodos [1]_
    as shown in [2]_.

    if \rho_r < 0.5:

    .. math::
        (\lambda-\lambda^\circ)\Gamma Z_c^5=1.22\times 10^{-2} [\exp(0.535 \rho_r)-1]

    if 0.5 < \rho_r < 2.0:

    .. math::
        (\lambda-\lambda^\circ)\Gamma Z_c^5=1.22\times 10^{-2} [\exp(0.535 \rho_r)-1]

    if 2 < \rho_r < 2.8:

    .. math::
        (\lambda-\lambda^\circ)\Gamma Z_c^5=1.22\times 10^{-2} [\exp(0.535 \rho_r)-1]

        \Gamma = 210 \left(\frac{T_cMW^3}{P_c^4}\right)^{1/6}

    Parameters
    ----------
    T : float
        Temperature of the gas [K]
    MW : float
        Molecular weight of the gas [g/mol]
    Tc : float
        Critical temperature of the gas [K]
    Pc : float
        Critical pressure of the gas [Pa]
    Vc : float
        Critical volume of the gas [m^3/mol]
    Zc : float
        Critical compressibility of the gas [-]
    Vm : float
        Molar volume of the gas at T and P [m^3/mol]
    kg : float
        Low-pressure gas thermal conductivity [W/m/k]

    Returns
    -------
    kg : float
        Estimated dense gas thermal conductivity [W/m/k]

    Notes
    -----
    Pc is internally converted to bar.

    Examples
    --------
    >>> stiel_thodos_dense(T=378.15, MW=44.013, Tc=309.6, Pc=72.4E5,
    ... Vc=97.4E-6, Zc=0.274, Vm=144E-6, kg=2.34E-2)
    0.041245574404863684

    References
    ----------
    .. [1] Stiel, Leonard I., and George Thodos. "The Thermal Conductivity of
       Nonpolar Substances in the Dense Gaseous and Liquid Regions." AIChE
       Journal 10, no. 1 (January 1, 1964): 26-30. doi:10.1002/aic.690100114.
    .. [2] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E.
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    gamma = 210*(Tc*MW**3./(Pc/1E5)**4)**(1/6.)
    rhor = Vc/Vm
    if rhor < 0.5:
        term = 1.22E-2*(exp(0.535*rhor) - 1.)
    elif rhor < 2:
        term = 1.14E-2*(exp(0.67*rhor) - 1.069)
    else:
        # Technically only up to 2.8
        term = 2.60E-3*(exp(1.155*rhor) + 2.016)
    diff = term/Zc**5/gamma
    kg = kg + diff
    return kg