def Campbell_Thodos(T, Tb, Tc, Pc, M, dipole=None, hydroxyl=False):
    r'''Calculate saturation liquid density using the Campbell-Thodos [1]_
    CSP method.

    An old and uncommon estimation method.

    .. math::
        V_s = \frac{RT_c}{P_c}{Z_{RA}}^{[1+(1-T_r)^{2/7}]}

        Z_{RA} = \alpha + \beta(1-T_r)

        \alpha = 0.3883-0.0179s

        s = T_{br} \frac{\ln P_c}{(1-T_{br})}

        \beta = 0.00318s-0.0211+0.625\Lambda^{1.35}

        \Lambda = \frac{P_c^{1/3}} { M^{1/2} T_c^{5/6}}

    For polar compounds:

    .. math::
        \theta = P_c \mu^2/T_c^2

        \alpha = 0.3883 - 0.0179s - 130540\theta^{2.41}

        \beta = 0.00318s - 0.0211 + 0.625\Lambda^{1.35} + 9.74\times
        10^6 \theta^{3.38}

    Polar Combounds with hydroxyl groups (water, alcohols)

    .. math::
        \alpha = \left[0.690T_{br} -0.3342 + \frac{5.79\times 10^{-10}}
        {T_{br}^{32.75}}\right] P_c^{0.145}

        \beta = 0.00318s - 0.0211 + 0.625 \Lambda^{1.35} + 5.90\Theta^{0.835}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    M : float
        Molecular weight of the fluid [g/mol]
    dipole : float, optional
        Dipole moment of the fluid [debye]
    hydroxyl : bool, optional
        Swith to use the hydroxyl variant for polar fluids

    Returns
    -------
    Vs : float
        Saturation liquid volume

    Notes
    -----
    If a dipole is provided, the polar chemical method is used.
    The paper is an excellent read.
    Pc is internally converted to atm.

    Examples
    --------
    Ammonia, from [1]_.

    >>> Campbell_Thodos(T=405.45, Tb=239.82, Tc=405.45, Pc=111.7*101325, M=17.03, dipole=1.47)
    7.347363635885525e-05

    References
    ----------
    .. [1] Campbell, Scott W., and George Thodos. "Prediction of Saturated
       Liquid Densities and Critical Volumes for Polar and Nonpolar
       Substances." Journal of Chemical & Engineering Data 30, no. 1
       (January 1, 1985): 102-11. doi:10.1021/je00039a032.
    '''
    Tr = T/Tc
    Tbr = Tb/Tc
    Pc = Pc/101325.
    s = Tbr * log(Pc)/(1-Tbr)
    Lambda = Pc**(1/3.)/(M**0.5*Tc**(5/6.))
    alpha = 0.3883 - 0.0179*s
    beta = 0.00318*s - 0.0211 + 0.625*Lambda**(1.35)
    if dipole:
        theta = Pc*dipole**2/Tc**2
        alpha -= 130540 * theta**2.41
        beta += 9.74E6 * theta**3.38
    if hydroxyl:
        beta = 0.00318*s - 0.0211 + 0.625*Lambda**(1.35) + 5.90*theta**0.835
        alpha = (0.69*Tbr - 0.3342 + 5.79E-10/Tbr**32.75)*Pc**0.145
    Zra = alpha + beta*(1-Tr)
    Vs = R*Tc/(Pc*101325)*Zra**(1+(1-Tr)**(2/7.))
    return Vs