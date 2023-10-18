def sigma_Tee_Gotoh_Steward_2(Tc, Pc, omega):
    r'''Calculates Lennard-Jones molecular diameter.
    Uses critical temperature, pressure, and acentric factor. CSP method by
    [1]_.

    .. math::
        \sigma = (2.3551 - 0.0874\omega)\left(\frac{T_c}{P_c}\right)^{1/3}

    Parameters
    ----------
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    omega : float
        Acentric factor for fluid, [-]

    Returns
    -------
    sigma : float
        Lennard-Jones molecular diameter, [Angstrom]

    Notes
    -----
    Original units of Pc are atm. Further regressions with other parameters
    were performed in [1]_ but are not included here, except for
    `sigma_Tee_Gotoh_Steward_1`.

    Examples
    --------
    >>> sigma_Tee_Gotoh_Steward_2(560.1, 4550000, 0.245)
    5.412104867264477

    References
    ----------
    .. [1] Tee, L. S., Sukehiro Gotoh, and W. E. Stewart. "Molecular Parameters
       for Normal Fluids. Lennard-Jones 12-6 Potential." Industrial
       & Engineering Chemistry Fundamentals 5, no. 3 (August 1, 1966): 356-63.
       doi:10.1021/i160019a011
    '''
    Pc = Pc/101325.
    sigma = (2.3551-0.0874*omega)*(Tc/Pc)**(1/3.)
    return sigma