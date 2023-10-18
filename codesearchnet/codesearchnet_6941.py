def lucas_gas(T, Tc, Pc, Zc, MW, dipole=0, CASRN=None):
    r'''Estimate the viscosity of a gas using an emperical
    formula developed in several sources, but as discussed in [1]_ as the
    original sources are in German or merely personal communications with the
    authors of [1]_.

    .. math::
        \eta  = \left[0.807T_r^{0.618}-0.357\exp(-0.449T_r) + 0.340\exp(-4.058
        T_r) + 0.018\right]F_p^\circ F_Q^\circ /\xi

        F_p^\circ=1, 0 \le \mu_{r} < 0.022

        F_p^\circ = 1+30.55(0.292-Z_c)^{1.72}, 0.022 \le \mu_{r} < 0.075

        F_p^\circ = 1+30.55(0.292-Z_c)^{1.72}|0.96+0.1(T_r-0.7)| 0.075 < \mu_{r}

        F_Q^\circ = 1.22Q^{0.15}\left\{ 1+0.00385[(T_r-12)^2]^{1/M}\text{sign}
        (T_r-12)\right\}

        \mu_r = 52.46 \frac{\mu^2 P_c}{T_c^2}

        \xi=0.176\left(\frac{T_c}{MW^3 P_c^4}\right)^{1/6}

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc: float
        Critical point of fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    Zc : float
        Critical compressibility of the fluid [Pa]
    dipole : float
        Dipole moment of fluid [debye]
    CASRN : str, optional
        CAS of the fluid

    Returns
    -------
    mu_g : float
        Viscosity of gas, [Pa*s]

    Notes
    -----
    The example is from [1]_; all results agree.
    Viscosity is calculated in micropoise, and converted to SI internally (1E-7).
    Q for He = 1.38; Q for H2 = 0.76; Q for D2 = 0.52.

    Examples
    --------
    >>> lucas_gas(T=550., Tc=512.6, Pc=80.9E5, Zc=0.224, MW=32.042, dipole=1.7)
    1.7822676912698928e-05

    References
    ----------
    .. [1] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E.
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    Tr = T/Tc
    xi = 0.176*(Tc/MW**3/(Pc/1E5)**4)**(1/6.)  # bar arrording to example in Poling
    if dipole is None:
        dipole = 0
    dipoler = 52.46*dipole**2*(Pc/1E5)/Tc**2  # bar arrording to example in Poling
    if dipoler < 0.022:
        Fp = 1
    elif 0.022 <= dipoler < 0.075:
        Fp = 1 + 30.55*(0.292 - Zc)**1.72
    else:
        Fp = 1 + 30.55*(0.292 - Zc)**1.72*abs(0.96 + 0.1*(Tr-0.7))
    if CASRN and CASRN in _lucas_Q_dict:
        Q = _lucas_Q_dict[CASRN]
        if Tr - 12 > 0:
            value = 1
        else:
            value = -1
        FQ = 1.22*Q**0.15*(1 + 0.00385*((Tr-12)**2)**(1./MW)*value)
    else:
        FQ = 1
    eta = (0.807*Tr**0.618 - 0.357*exp(-0.449*Tr) + 0.340*exp(-4.058*Tr) + 0.018)*Fp*FQ/xi
    return eta/1E7