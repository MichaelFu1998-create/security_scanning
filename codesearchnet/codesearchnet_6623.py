def TRCCp_integral(T, a0, a1, a2, a3, a4, a5, a6, a7, I=0):
    r'''Integrates ideal gas heat capacity using the model developed in [1]_.
    Best used as a delta only.

    The difference in enthalpy with respect to 0 K is given by:

    .. math::
        \frac{H(T) - H^{ref}}{RT} = a_0 + a_1x(a_2)/(a_2T) + I/T + h(T)/T
        
        h(T) = (a_5 + a_7)\left[(2a_3 + 8a_4)\ln(1-y)+ \left\{a_3\left(1 + 
        \frac{1}{1-y}\right) + a_4\left(7 + \frac{1}{1-y}\right)\right\}y
        + a_4\left\{3y^2 + (5/3)y^3 + y^4 + (3/5)y^5 + (1/3)y^6\right\} 
        + (1/7)\left\{a_4 - \frac{a_5}{(a_6+a_7)^2}\right\}y^7\right]
        
        h(T) = 0 \text{ for } T \le a_7

        y = \frac{T-a_7}{T+a_6} \text{ for } T > a_7 \text{ otherwise } 0

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a7 : float
        Coefficients
    I : float, optional
        Integral offset

    Returns
    -------
    H-H(0) : float
        Difference in enthalpy from 0 K , [J/mol]

    Notes
    -----
    Analytical integral as provided in [1]_ and verified with numerical
    integration. 

    Examples
    --------
    >>> TRCCp_integral(298.15, 4.0, 7.65E5, 720., 3.565, -0.052, -1.55E6, 52., 
    ... 201., 1.2)
    10802.532600592816
    
    References
    ----------
    .. [1] Kabo, G. J., and G. N. Roganov. Thermodynamics of Organic Compounds
       in the Gas State, Volume II: V. 2. College Station, Tex: CRC Press, 1994.
    '''
    if T <= a7:
        y = 0.
    else:
        y = (T - a7)/(T + a6)
    y2 = y*y
    y4 = y2*y2
    if T <= a7:
        h = 0.0
    else:
        first = a6 + a7
        second = (2.*a3 + 8.*a4)*log(1. - y)
        third = (a3*(1. + 1./(1. - y)) + a4*(7. + 1./(1. - y)))*y
        fourth = a4*(3.*y2 + 5./3.*y*y2 + y4 + 0.6*y4*y + 1/3.*y4*y2)
        fifth = 1/7.*(a4 - a5/((a6 + a7)**2))*y4*y2*y
        h = first*(second + third + fourth + fifth)
    return (a0 + a1*exp(-a2/T)/(a2*T) + I/T + h/T)*R*T