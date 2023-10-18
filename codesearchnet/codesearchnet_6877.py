def Zuo_Stenby(T, Tc, Pc, omega):
    r'''Calculates air-water surface tension using the reference fluids
    methods of [1]_.

    .. math::
        \sigma^{(1)} = 40.520(1-T_r)^{1.287}
        \sigma^{(2)} = 52.095(1-T_r)^{1.21548}
        \sigma_r = \sigma_r^{(1)}+ \frac{\omega - \omega^{(1)}}
        {\omega^{(2)}-\omega^{(1)}} (\sigma_r^{(2)}-\sigma_r^{(1)})
        \sigma = T_c^{1/3}P_c^{2/3}[\exp{(\sigma_r)} -1]

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    omega : float
        Acentric factor for fluid, [-]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m

    Notes
    -----
    Presently untested. Have not personally checked the sources.
    I strongly believe it is broken.
    The reference values for methane and n-octane are from the DIPPR database.

    Examples
    --------
    Chlorobenzene

    >>> Zuo_Stenby(293., 633.0, 4530000.0, 0.249)
    0.03345569011871088

    References
    ----------
    .. [1] Zuo, You-Xiang, and Erling H. Stenby. "Corresponding-States and
       Parachor Models for the Calculation of Interfacial Tensions." The
       Canadian Journal of Chemical Engineering 75, no. 6 (December 1, 1997):
       1130-37. doi:10.1002/cjce.5450750617
    '''
    Tc_1, Pc_1, omega_1 = 190.56, 4599000.0/1E5, 0.012
    Tc_2, Pc_2, omega_2 = 568.7, 2490000.0/1E5, 0.4
    Pc = Pc/1E5

    def ST_r(ST, Tc, Pc):
        return log(1 + ST/(Tc**(1/3.0)*Pc**(2/3.0)))

    ST_1 = 40.520*(1 - T/Tc)**1.287  # Methane
    ST_2 = 52.095*(1 - T/Tc)**1.21548  # n-octane

    ST_r_1, ST_r_2 = ST_r(ST_1, Tc_1, Pc_1), ST_r(ST_2, Tc_2, Pc_2)

    sigma_r = ST_r_1 + (omega-omega_1)/(omega_2 - omega_1)*(ST_r_2-ST_r_1)
    sigma = Tc**(1/3.0)*Pc**(2/3.0)*(exp(sigma_r)-1)
    sigma = sigma/1000  # N/m, please
    return sigma