def REFPROP(T, Tc, sigma0, n0, sigma1=0, n1=0, sigma2=0, n2=0):
    r'''Calculates air-liquid surface tension  using the REFPROP [1]_
    regression-based method. Relatively recent, and most accurate.

    .. math::
        \sigma(T)=\sigma_0\left(1-\frac{T}{T_c}\right)^{n_0}+
        \sigma_1\left(1-\frac{T}{T_c}\right)^{n_1}+
        \sigma_2\left(1-\frac{T}{T_c}\right)^{n_2}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    sigma0 : float
        First emperical coefficient of a fluid
    n0 : float
        First emperical exponent of a fluid
    sigma1 : float, optional
        Second emperical coefficient of a fluid.
    n1 : float, optional
        Second emperical exponent of a fluid.
    sigma1 : float, optional
        Third emperical coefficient of a fluid.
    n2 : float, optional
        Third emperical exponent of a fluid.

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    Function as implemented in [1]_. No example necessary; results match
    literature values perfectly.
    Form of function returns imaginary results when T > Tc; None is returned
    if this is the case.


    Examples
    --------
    Parameters for water at 298.15 K

    >>> REFPROP(298.15, 647.096, -0.1306, 2.471, 0.2151, 1.233)
    0.07205503890847453

    References
    ----------
    .. [1] Diky, Vladimir, Robert D. Chirico, Chris D. Muzny, Andrei F.
       Kazakov, Kenneth Kroenlein, Joseph W. Magee, Ilmutdin Abdulagatov, and
       Michael Frenkel. "ThermoData Engine (TDE): Software Implementation of
       the Dynamic Data Evaluation Concept." Journal of Chemical Information
       and Modeling 53, no. 12 (2013): 3418-30. doi:10.1021/ci4005699.
    '''
    Tr = T/Tc
    sigma = sigma0*(1.-Tr)**n0 + sigma1*(1.-Tr)**n1 + sigma2*(1.-Tr)**n2
    return sigma