def Lucas(T, P, Tc, Pc, omega, P_sat, mu_l):
    r'''Adjustes for pressure the viscosity of a liquid using an emperical
    formula developed in [1]_, but as discussed in [2]_ as the original source
    is in German.

    .. math::
        \frac{\mu}{\mu_{sat}}=\frac{1+D(\Delta P_r/2.118)^A}{1+C\omega \Delta P_r}

        \Delta P_r = \frac{P-P^{sat}}{P_c}

        A=0.9991-\frac{4.674\times 10^{-4}}{1.0523T_r^{-0.03877}-1.0513}

        D = \frac{0.3257}{(1.0039-T_r^{2.573})^{0.2906}}-0.2086

        C = -0.07921+2.1616T_r-13.4040T_r^2+44.1706T_r^3-84.8291T_r^4+
        96.1209T_r^5-59.8127T_r^6+15.6719T_r^7

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
    omega : float
        Acentric factor of compound
    P_sat : float
        Saturation pressure of the fluid [Pa]
    mu_l : float
        Viscosity of liquid at 1 atm or saturation, [Pa*S]

    Returns
    -------
    mu_l_dense : float
        Viscosity of liquid, [Pa*s]

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    The example is from Reid (1987); all results agree.
    Above several thousand bar, this equation does not represent true behavior.
    If Psat is larger than P, the fluid may not be liquid; dPr is set to 0.

    Examples
    --------
    >>> Lucas(300., 500E5, 572.2, 34.7E5, 0.236, 0, 0.00068) # methylcyclohexane
    0.0010683738499316518

    References
    ----------
    .. [1] Lucas, Klaus. "Ein Einfaches Verfahren Zur Berechnung Der
       Viskositat von Gasen Und Gasgemischen." Chemie Ingenieur Technik 46, no. 4
       (February 1, 1974): 157-157. doi:10.1002/cite.330460413.
    .. [2] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E.
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    '''
    Tr = T/Tc
    C = -0.07921+2.1616*Tr - 13.4040*Tr**2 + 44.1706*Tr**3 - 84.8291*Tr**4 \
        + 96.1209*Tr**5-59.8127*Tr**6+15.6719*Tr**7
    D = 0.3257/((1.0039-Tr**2.573)**0.2906) - 0.2086
    A = 0.9991 - 4.674E-4/(1.0523*Tr**-0.03877 - 1.0513)
    dPr = (P-P_sat)/Pc
    if dPr < 0:
        dPr = 0
    return (1. + D*(dPr/2.118)**A)/(1. + C*omega*dPr)*mu_l