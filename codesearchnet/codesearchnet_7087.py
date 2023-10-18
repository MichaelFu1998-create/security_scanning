def DIPPR9B(T, MW, Cvm, mu, Tc=None, chemtype=None):
    r'''Calculates the thermal conductivity of a gas using one of several
    emperical equations developed in [1]_, [2]_, and presented in [3]_.

    For monoatomic gases:

    .. math::
        k = 2.5 \frac{\eta C_v}{MW}

    For linear molecules:

    .. math::
        k = \frac{\eta}{MW} \left( 1.30 C_v + 14644.00 - \frac{2928.80}{T_r}\right)

    For nonlinear molecules:

    .. math::
        k = \frac{\eta}{MW}(1.15C_v + 16903.36)

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    Tc : float
        Critical temperature of the fluid [K]
    MW : float
        Molwcular weight of fluid [g/mol]
    Cvm : float
        Molar heat capacity at constant volume of fluid, [J/mol/K]
    mu : float
        Viscosity of gas, [Pa*S]

    Returns
    -------
    k_g : float
        Thermal conductivity of gas, [W/m/k]

    Notes
    -----
    Tested with DIPPR values.
    Cvm is internally converted to J/kmol/K.

    Examples
    --------
    CO:

    >>> DIPPR9B(200., 28.01, 20.826, 1.277E-5, 132.92, chemtype='linear')
    0.01813208676438415

    References
    ----------
    .. [1] Bromley, LeRoy A., Berkeley. University of California, and U.S.
       Atomic Energy Commission. Thermal Conductivity of Gases at Moderate
       Pressures. UCRL;1852. Berkeley, CA: University of California Radiation
       Laboratory, 1952.
    .. [2] Stiel, Leonard I., and George Thodos. "The Thermal Conductivity of
       Nonpolar Substances in the Dense Gaseous and Liquid Regions." AIChE
       Journal 10, no. 1 (January 1, 1964): 26-30. doi:10.1002/aic.690100114
    .. [3] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    Cvm = Cvm*1000.  # J/g/K to J/kmol/K
    if not chemtype:
        chemtype = 'linear'
    if chemtype == 'monoatomic':
        return 2.5*mu*Cvm/MW
    elif chemtype == 'linear':
        Tr = T/Tc
        return mu/MW*(1.30*Cvm + 14644 - 2928.80/Tr)
    elif chemtype == 'nonlinear':
        return mu/MW*(1.15*Cvm + 16903.36)
    else:
        raise Exception('Specified chemical type is not an option')