def MK(T, Tc, omega):
    r'''Calculates enthalpy of vaporization at arbitrary temperatures using a
    the work of [1]_; requires a chemical's critical temperature and
    acentric factor.

    The enthalpy of vaporization is given by:

    .. math::
        \Delta H_{vap} =  \Delta H_{vap}^{(0)} + \omega \Delta H_{vap}^{(1)} + \omega^2 \Delta H_{vap}^{(2)}

        \frac{\Delta H_{vap}^{(i)}}{RT_c} = b^{(j)} \tau^{1/3} + b_2^{(j)} \tau^{5/6}
        + b_3^{(j)} \tau^{1.2083} + b_4^{(j)}\tau + b_5^{(j)} \tau^2 + b_6^{(j)} \tau^3

        \tau = 1-T/T_c

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    omega : float
        Acentric factor [-]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    The original article has been reviewed. A total of 18 coefficients are used:

    WARNING: The correlation has been implemented as described in the article,
    but its results seem different and with some error.
    Its results match with other functions however.

    Has poor behavior for low-temperature use.

    Examples
    --------
    Problem in article for SMK function.

    >>> MK(553.15, 751.35, 0.302)
    38727.993546377205

    References
    ----------
    .. [1] Morgan, David L., and Riki Kobayashi. "Extension of Pitzer CSP
       Models for Vapor Pressures and Heats of Vaporization to Long-Chain
       Hydrocarbons." Fluid Phase Equilibria 94 (March 15, 1994): 51-87.
       doi:10.1016/0378-3812(94)87051-9.
    '''
    bs = [[5.2804, 0.080022, 7.2543],
          [12.8650, 273.23, -346.45],
          [1.1710, 465.08, -610.48],
          [-13.1160, -638.51, 839.89],
          [0.4858, -145.12, 160.05],
          [-1.0880, 74.049, -50.711]]

    tau = 1. - T/Tc
    H0 = (bs[0][0]*tau**(0.3333) + bs[1][0]*tau**(0.8333) + bs[2][0]*tau**(1.2083) +
    bs[3][0]*tau + bs[4][0]*tau**(2) + bs[5][0]*tau**(3))*R*Tc

    H1 = (bs[0][1]*tau**(0.3333) + bs[1][1]*tau**(0.8333) + bs[2][1]*tau**(1.2083) +
    bs[3][1]*tau + bs[4][1]*tau**(2) + bs[5][1]*tau**(3))*R*Tc

    H2 = (bs[0][2]*tau**(0.3333) + bs[1][2]*tau**(0.8333) + bs[2][2]*tau**(1.2083) +
    bs[3][2]*tau + bs[4][2]*tau**(2) + bs[5][2]*tau**(3))*R*Tc

    return H0 + omega*H1 + omega**2*H2