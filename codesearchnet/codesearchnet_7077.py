def Nicola_original(T, M, Tc, omega, Hfus):
    r'''Estimates the thermal conductivity of a liquid as a function of
    temperature using the CSP method of Nicola [1]_. A  simpler but long
    method claiming high-accuracy and using only statistically significant
    variable following analalysis.

    Requires temperature, molecular weight, critical temperature, acentric
    factor and the heat of vaporization.

    .. math::
        \frac{\lambda}{1 \text{Wm/K}}=-0.5694-0.1436T_r+5.4893\times10^{-10}
        \frac{\Delta_{fus}H}{\text{kmol/J}}+0.0508\omega +
        \left(\frac{1 \text{kg/kmol}}{MW}\right)^{0.0622}

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    M : float
        Molecular weight of the fluid [g/mol]
    Tc : float
        Critical temperature of the fluid [K]
    omega : float
        Acentric factor of the fluid [-]
    Hfus : float
        Heat of fusion of the fluid [J/mol]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k]

    Notes
    -----
    A weird statistical correlation. Recent and yet to be reviewed.
    This correlation has been superceded by the author's later work.
    Hfus is internally converted to be in J/kmol.

    Examples
    --------
    >>> Nicola_original(300, 142.3, 611.7, 0.49, 201853)
    0.2305018632230984

    References
    ----------
    .. [1] Nicola, Giovanni Di, Eleonora Ciarrocchi, Mariano Pierantozzi, and
        Roman Stryjek. "A New Equation for the Thermal Conductivity of Organic
        Compounds." Journal of Thermal Analysis and Calorimetry 116, no. 1
        (April 1, 2014): 135-40. doi:10.1007/s10973-013-3422-7
    '''
    Tr = T/Tc
    Hfus = Hfus*1000
    return -0.5694 - 0.1436*Tr + 5.4893E-10*Hfus + 0.0508*omega + (1./M)**0.0622