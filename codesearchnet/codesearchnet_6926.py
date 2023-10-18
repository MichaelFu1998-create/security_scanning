def sigma_Silva_Liu_Macedo(Tc, Pc):
    r'''Calculates Lennard-Jones molecular diameter.
    Uses critical temperature and pressure. CSP method by [1]_.

    .. math::
        \sigma_{LJ}^3 = 0.17791 + 11.779 \left( \frac{T_c}{P_c}\right)
        - 0.049029\left( \frac{T_c}{P_c}\right)^2

    Parameters
    ----------
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    sigma : float
        Lennard-Jones molecular diameter, [Angstrom]

    Notes
    -----
    Pc is originally in bar. An excellent paper. None is  
    returned if the polynomial returns a negative number, as in the case of 
    1029.13 K and 3.83 bar.

    Examples
    --------
    >>> sigma_Silva_Liu_Macedo(560.1, 4550000)
    5.164483998730177

    References
    ----------
    .. [1] Silva, Carlos M., Hongqin Liu, and Eugenia A. Macedo. "Models for
       Self-Diffusion Coefficients of Dense Fluids, Including Hydrogen-Bonding
       Substances." Chemical Engineering Science 53, no. 13 (July 1, 1998):
       2423-29. doi:10.1016/S0009-2509(98)00037-2
    '''
    Pc = Pc/1E5  # Pa to bar
    term = 0.17791 + 11.779*(Tc/Pc) - 0.049029 * (Tc/Pc)**2
    if term < 0:
        sigma = None
    else:
        sigma = (term)**(1/3.)
    return sigma