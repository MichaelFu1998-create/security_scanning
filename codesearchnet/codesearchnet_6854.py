def Laliberte_density_i(T, w_w, c0, c1, c2, c3, c4):
    r'''Calculate the density of a solute using the form proposed by Laliberte [1]_.
    Parameters are needed, and a temperature, and water fraction. Units are Kelvin and Pa*s.

    .. math::
        \rho_{app,i} = \frac{(c_0[1-w_w]+c_1)\exp(10^{-6}[t+c_4]^2)}
        {(1-w_w) + c_2 + c_3 t}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    w_w : float
        Weight fraction of water in the solution
    c0-c4 : floats
        Function fit parameters

    Returns
    -------
    rho_i : float
        Solute partial density, [kg/m^3]

    Notes
    -----
    Temperature range check is TODO


    Examples
    --------
    >>> d = _Laliberte_Density_ParametersDict['7647-14-5']
    >>> Laliberte_density_i(273.15+0, 1-0.0037838838, d["C0"], d["C1"], d["C2"], d["C3"], d["C4"])
    3761.8917585699983

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    t = T - 273.15
    return ((c0*(1 - w_w)+c1)*exp(1E-6*(t + c4)**2))/((1 - w_w) + c2 + c3*t)