def Laliberte_viscosity(T, ws, CASRNs):
    r'''Calculate the viscosity of an aqueous mixture using the form proposed by [1]_.
    Parameters are loaded by the function as needed. Units are Kelvin and Pa*s.

    .. math::
        \mu_m = \mu_w^{w_w} \Pi\mu_i^{w_i}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    ws : array
        Weight fractions of fluid components other than water
    CASRNs : array
        CAS numbers of the fluid components other than water

    Returns
    -------
    mu_i : float
        Solute partial viscosity, Pa*s

    Notes
    -----
    Temperature range check is not used here.
    Check is performed using NaCl at 5 degC from the first value in [1]_'s spreadsheet.

    Examples
    --------
    >>> Laliberte_viscosity(273.15+5, [0.005810], ['7647-14-5'])
    0.0015285828581961414

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    mu_w = Laliberte_viscosity_w(T)*1000.
    w_w = 1 - sum(ws)
    mu = mu_w**(w_w)
    for i in range(len(CASRNs)):
        d = _Laliberte_Viscosity_ParametersDict[CASRNs[i]]
        mu_i = Laliberte_viscosity_i(T, w_w, d["V1"], d["V2"], d["V3"], d["V4"], d["V5"], d["V6"])*1000.
        mu = mu_i**(ws[i])*mu
    return mu/1000.