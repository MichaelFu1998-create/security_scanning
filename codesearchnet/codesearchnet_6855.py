def Laliberte_density(T, ws, CASRNs):
    r'''Calculate the density of an aqueous electrolyte mixture using the form proposed by [1]_.
    Parameters are loaded by the function as needed. Units are Kelvin and Pa*s.

    .. math::
        \rho_m = \left(\frac{w_w}{\rho_w} + \sum_i \frac{w_i}{\rho_{app_i}}\right)^{-1}

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
    rho_i : float
        Solution density, [kg/m^3]

    Notes
    -----
    Temperature range check is not used here.

    Examples
    --------
    >>> Laliberte_density(273.15, [0.0037838838], ['7647-14-5'])
    1002.6250120185854

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    rho_w = Laliberte_density_w(T)
    w_w = 1 - sum(ws)
    rho = w_w/rho_w
    for i in range(len(CASRNs)):
        d = _Laliberte_Density_ParametersDict[CASRNs[i]]
        rho_i = Laliberte_density_i(T, w_w, d["C0"], d["C1"], d["C2"], d["C3"], d["C4"])
        rho = rho + ws[i]/rho_i
    return 1./rho