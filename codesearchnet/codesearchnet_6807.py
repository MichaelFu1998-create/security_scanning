def Townsend_Hales(T, Tc, Vc, omega):
    r'''Calculates saturation liquid density, using the Townsend and Hales
    CSP method as modified from the original Riedel equation. Uses
    chemical critical volume and temperature, as well as acentric factor

    The density of a liquid is given by:

    .. math::
        Vs = V_c/\left(1+0.85(1-T_r)+(1.692+0.986\omega)(1-T_r)^{1/3}\right)

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Vc : float
        Critical volume of fluid [m^3/mol]
    omega : float
        Acentric factor for fluid, [-]

    Returns
    -------
    Vs : float
        Saturation liquid volume, [m^3/mol]

    Notes
    -----
    The requirement for critical volume and acentric factor requires all data.

    Examples
    --------
    >>> Townsend_Hales(300, 647.14, 55.95E-6, 0.3449)
    1.8007361992619923e-05

    References
    ----------
    .. [1] Hales, J. L, and R Townsend. "Liquid Densities from 293 to 490 K of
       Nine Aromatic Hydrocarbons." The Journal of Chemical Thermodynamics
       4, no. 5 (1972): 763-72. doi:10.1016/0021-9614(72)90050-X
    '''
    Tr = T/Tc
    return Vc/(1 + 0.85*(1-Tr) + (1.692 + 0.986*omega)*(1-Tr)**(1/3.))