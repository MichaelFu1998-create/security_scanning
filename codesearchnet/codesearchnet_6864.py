def Kweq_IAPWS_gas(T):
    r'''Calculates equilibrium constant for OH- and H+ in water vapor,
    according to [1]_.
    This is the most recent formulation available.

    .. math::
        -log_{10}  K_w^G = \gamma_0 + \gamma_1 T^{-1} + \gamma_2 T^{-2} + \gamma_3 T^{-3}

    Parameters
    ----------
    T : float
        Temperature of H2O [K]

    Returns
    -------
    K_w_G : float

    Notes
    -----
    gamma0 = 6.141500E-1; 
    gamma1 = 4.825133E4; 
    gamma2 = -6.770793E4; 
    gamma3 = 1.010210E7

    Examples
    --------
    >>> Kweq_IAPWS_gas(800)
    1.4379721554798815e-61
    
    References
    ----------
    .. [1] Bandura, Andrei V., and Serguei N. Lvov. "The Ionization Constant
       of Water over Wide Ranges of Temperature and Density." Journal of Physical
       and Chemical Reference Data 35, no. 1 (March 1, 2006): 15-30.
       doi:10.1063/1.1928231
    '''
    gamma0 = 6.141500E-1
    gamma1 = 4.825133E4
    gamma2 = -6.770793E4
    gamma3 = 1.010210E7
    K_w_G = 10**(-1*(gamma0 + gamma1/T + gamma2/T**2 + gamma3/T**3))
    return K_w_G