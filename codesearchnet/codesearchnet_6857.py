def Laliberte_heat_capacity(T, ws, CASRNs):
    r'''Calculate the heat capacity of an aqueous electrolyte mixture using the
    form proposed by [1]_.
    Parameters are loaded by the function as needed.

    .. math::
        TODO

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
    Cp : float
        Solution heat capacity, [J/kg/K]

    Notes
    -----
    Temperature range check is not implemented.
    Units are Kelvin and J/kg/K.

    Examples
    --------
    >>> Laliberte_heat_capacity(273.15+1.5, [0.00398447], ['7647-14-5']) 
    4186.569908672113

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    Cp_w = Laliberte_heat_capacity_w(T)
    w_w = 1 - sum(ws)
    Cp = w_w*Cp_w

    for i in range(len(CASRNs)):
        d = _Laliberte_Heat_Capacity_ParametersDict[CASRNs[i]]
        Cp_i = Laliberte_heat_capacity_i(T, w_w, d["A1"], d["A2"], d["A3"], d["A4"], d["A5"], d["A6"])
        Cp = Cp + ws[i]*Cp_i
    return Cp