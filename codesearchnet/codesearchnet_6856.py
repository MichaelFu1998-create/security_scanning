def Laliberte_heat_capacity_i(T, w_w, a1, a2, a3, a4, a5, a6):
    r'''Calculate the heat capacity of a solute using the form proposed by [1]_
    Parameters are needed, and a temperature, and water fraction.

    .. math::
        Cp_i = a_1 e^\alpha + a_5(1-w_w)^{a_6}
        \alpha = a_2 t + a_3 \exp(0.01t) + a_4(1-w_w)

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    w_w : float
        Weight fraction of water in the solution
    a1-a6 : floats
        Function fit parameters

    Returns
    -------
    Cp_i : float
        Solute partial heat capacity, [J/kg/K]

    Notes
    -----
    Units are Kelvin and J/kg/K.
    Temperature range check is TODO

    Examples
    --------
    >>> d = _Laliberte_Heat_Capacity_ParametersDict['7647-14-5']
    >>> Laliberte_heat_capacity_i(1.5+273.15, 1-0.00398447, d["A1"], d["A2"], d["A3"], d["A4"], d["A5"], d["A6"])
    -2930.7353945880477

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    t = T - 273.15
    alpha = a2*t + a3*exp(0.01*t) + a4*(1. - w_w)
    Cp_i = a1*exp(alpha) + a5*(1. - w_w)**a6
    return Cp_i*1000.