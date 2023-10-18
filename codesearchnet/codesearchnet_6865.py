def Kweq_IAPWS(T, rho_w):
    r'''Calculates equilibrium constant for OH- and H+ in water, according to
    [1]_.
    This is the most recent formulation available.

    .. math::
        Q = \rho \exp(\alpha_0 + \alpha_1 T^{-1} + \alpha_2 T^{-2} \rho^{2/3})
        
        - \log_{10} K_w = -2n \left[ \log_{10}(1+Q) - \frac{Q}{Q+1} \rho 
        (\beta_0 + \beta_1 T^{-1} + \beta_2 \rho) \right]
        -\log_{10} K_w^G + 2 \log_{10} \frac{18.015268}{1000}

    Parameters
    ----------
    T : float
        Temperature of water [K]
    rho_w : float
        Density of water at temperature and pressure [kg/m^3]

    Returns
    -------
    Kweq : float
        Ionization constant of water, [-]

    Notes
    -----
    Formulation is in terms of density in g/cm^3; density
    is converted internally.
    
    n = 6;
    alpha0 = -0.864671;
    alpha1 = 8659.19;
    alpha2 = -22786.2;
    beta0 = 0.642044;
    beta1 = -56.8534;
    beta2 = -0.375754

    Examples
    --------
    Example from IAPWS check:
    
    >>> -1*log10(Kweq_IAPWS(600, 700))
    11.203153057603775

    References
    ----------
    .. [1] Bandura, Andrei V., and Serguei N. Lvov. "The Ionization Constant
       of Water over Wide Ranges of Temperature and Density." Journal of Physical
       and Chemical Reference Data 35, no. 1 (March 1, 2006): 15-30.
       doi:10.1063/1.1928231
    '''
    K_w_G = Kweq_IAPWS_gas(T)
    rho_w = rho_w/1000.
    n = 6
    alpha0 = -0.864671
    alpha1 = 8659.19
    alpha2 = -22786.2
    beta0 = 0.642044
    beta1 = -56.8534
    beta2 = -0.375754

    Q = rho_w*exp(alpha0 + alpha1/T + alpha2/T**2*rho_w**(2/3.))
    K_w = 10**(-1*(-2*n*(log10(1+Q)-Q/(Q+1) * rho_w *(beta0 + beta1/T + beta2*rho_w)) -
    log10(K_w_G) + 2*log10(18.015268/1000) ))
    return K_w