def Laliberte_density_w(T):
    r'''Calculate the density of water using the form proposed by [1]_.
    No parameters are needed, just a temperature. Units are Kelvin and kg/m^3h.

    .. math::
        \rho_w = \frac{\left\{\left([(-2.8054253\times 10^{-10}\cdot t +
        1.0556302\times 10^{-7})t - 4.6170461\times 10^{-5}]t
        -0.0079870401\right)t + 16.945176   \right\}t + 999.83952}
        {1 + 0.01687985\cdot t}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]

    Returns
    -------
    rho_w : float
        Water density, [kg/m^3]

    Notes
    -----
    Original source not cited
    No temperature range is used.

    Examples
    --------
    >>> Laliberte_density_w(298.15)
    997.0448954179155
    >>> Laliberte_density_w(273.15 + 50)
    988.0362916114763

    References
    ----------
    .. [1] Laliberte, Marc. "A Model for Calculating the Heat Capacity of
       Aqueous Solutions, with Updated Density and Viscosity Data." Journal of
       Chemical & Engineering Data 54, no. 6 (June 11, 2009): 1725-60.
       doi:10.1021/je8008123
    '''
    t = T-273.15
    rho_w = (((((-2.8054253E-10*t + 1.0556302E-7)*t - 4.6170461E-5)*t - 0.0079870401)*t + 16.945176)*t + 999.83952) \
        / (1 + 0.01687985*t)
    return rho_w