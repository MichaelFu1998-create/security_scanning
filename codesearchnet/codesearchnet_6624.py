def TRCCp_integral_over_T(T, a0, a1, a2, a3, a4, a5, a6, a7, J=0):
    r'''Integrates ideal gas heat capacity over T using the model developed in 
    [1]_. Best used as a delta only.

    The difference in ideal-gas entropy with respect to 0 K is given by:

    .. math::
        \frac{S^\circ}{R} = J + a_0\ln T + \frac{a_1}{a_2^2}\left(1
        + \frac{a_2}{T}\right)x(a_2) + s(T)

        s(T) = \left[\left\{a_3 + \left(\frac{a_4 a_7^2 - a_5}{a_6^2}\right)
        \left(\frac{a_7}{a_6}\right)^4\right\}\left(\frac{a_7}{a_6}\right)^2
        \ln z + (a_3 + a_4)\ln\left(\frac{T+a_6}{a_6+a_7}\right)
        +\sum_{i=1}^7 \left\{\left(\frac{a_4 a_7^2 - a_5}{a_6^2}\right)\left(
        \frac{-a_7}{a_6}\right)^{6-i} - a_4\right\}\frac{y^i}{i}
        - \left\{\frac{a_3}{a_6}(a_6 + a_7) + \frac{a_5 y^6}{7a_7(a_6+a_7)}
        \right\}y\right]

        s(T) = 0 \text{ for } T \le a_7
        
        z = \frac{T}{T+a_6} \cdot \frac{a_7 + a_6}{a_7}

        y = \frac{T-a_7}{T+a_6} \text{ for } T > a_7 \text{ otherwise } 0

    Parameters
    ----------
    T : float
        Temperature [K]
    a1-a7 : float
        Coefficients
    J : float, optional
        Integral offset

    Returns
    -------
    S-S(0) : float
        Difference in entropy from 0 K , [J/mol/K]

    Notes
    -----
    Analytical integral as provided in [1]_ and verified with numerical
    integration. 

    Examples
    --------
    >>> TRCCp_integral_over_T(300, 4.0, 124000, 245, 50.539, -49.469, 
    ... 220440000, 560, 78)
    213.80148972435018
    
    References
    ----------
    .. [1] Kabo, G. J., and G. N. Roganov. Thermodynamics of Organic Compounds
       in the Gas State, Volume II: V. 2. College Station, Tex: CRC Press, 1994.
    '''
    # Possible optimizations: pre-cache as much as possible.
    # If this were replaced by a cache, much of this would not need to be computed.
    if T <= a7:
        y = 0.
    else:
        y = (T - a7)/(T + a6)

    z = T/(T + a6)*(a7 + a6)/a7
    if T <= a7:
        s = 0.
    else:
        a72 = a7*a7
        a62 = a6*a6
        a7_a6 = a7/a6 # a7/a6
        a7_a6_2 = a7_a6*a7_a6
        a7_a6_4 = a7_a6_2*a7_a6_2
        x1 = (a4*a72 - a5)/a62 # part of third, sum
        first = (a3 + ((a4*a72 - a5)/a62)*a7_a6_4)*a7_a6_2*log(z)
        second = (a3 + a4)*log((T + a6)/(a6 + a7))
        fourth = -(a3/a6*(a6 + a7) + a5*y**6/(7.*a7*(a6 + a7)))*y
        third = sum([(x1*(-a7_a6)**(6-i) - a4)*y**i/i for i in range(1, 8)])
        s = first + second + third + fourth
    return R*(J + a0*log(T) + a1/(a2*a2)*(1. + a2/T)*exp(-a2/T) + s)