def DIPPR9G(T, P, Tc, Pc, kl):
    r'''Adjustes for pressure the thermal conductivity of a liquid using an
    emperical formula based on [1]_, but as given in [2]_.

    .. math::
        k = k^* \left[ 0.98 + 0.0079 P_r T_r^{1.4} + 0.63 T_r^{1.2}
        \left( \frac{P_r}{30 + P_r}\right)\right]

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    P : float
        Pressure of fluid [Pa]
    Tc: float
        Critical point of fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]
    kl : float
        Thermal conductivity of liquid at 1 atm or saturation, [W/m/K]

    Returns
    -------
    kl_dense : float
        Thermal conductivity of liquid at P, [W/m/K]

    Notes
    -----
    This equation is entrely dimensionless; all dimensions cancel.
    The original source has not been reviewed.

    This is DIPPR Procedure 9G: Method for the Thermal Conductivity of Pure
    Nonhydrocarbon Liquids at High Pressures

    Examples
    --------
    From [2]_, for butyl acetate.

    >>> DIPPR9G(515.05, 3.92E7, 579.15, 3.212E6, 7.085E-2)
    0.0864419738671184

    References
    ----------
    .. [1] Missenard, F. A., Thermal Conductivity of Organic Liquids of a
       Series or a Group of Liquids , Rev. Gen.Thermodyn., 101 649 (1970).
    .. [2] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    Tr = T/Tc
    Pr = P/Pc
    return kl*(0.98 + 0.0079*Pr*Tr**1.4 + 0.63*Tr**1.2*(Pr/(30. + Pr)))