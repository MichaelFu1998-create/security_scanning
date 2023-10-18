def Laliberte_viscosity_i(T, w_w, v1, v2, v3, v4, v5, v6):
    r'''Calculate the viscosity of a solute using the form proposed by [1]_
    Parameters are needed, and a temperature. Units are Kelvin and Pa*s.

    .. math::
        \mu_i = \frac{\exp\left( \frac{v_1(1-w_w)^{v_2}+v_3}{v_4 t +1}\right)}
            {v_5(1-w_w)^{v_6}+1}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    w_w : float
        Weight fraction of water in the solution
    v1-v6 : floats
        Function fit parameters

    Returns
    -------
    mu_i : float
        Solute partial viscosity, Pa*s

    Notes
    -----
    Temperature range check is outside of this function.
    Check is performed using NaCl at 5 degC from the first value in [1]_'s spreadsheet.

    Examples
    --------
    >>> d =  _Laliberte_Viscosity_ParametersDict['7647-14-5']
    >>> Laliberte_viscosity_i(273.15+5, 1-0.005810, d["V1"], d["V2"], d["V3"], d["V4"], d["V5"], d["V6"] )
    0.004254025533308794

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    t = T-273.15
    mu_i = exp((v1*(1-w_w)**v2 + v3)/(v4*t+1))/(v5*(1-w_w)**v6 + 1)
    return mu_i/1000.