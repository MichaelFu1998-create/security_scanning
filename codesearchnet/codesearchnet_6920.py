def EQ116(T, Tc, A, B, C, D, E, order=0):
    r'''DIPPR Equation #116. Used to describe the molar density of water fairly
    precisely; no other uses listed. All 5 parameters are needed, as well as
    the critical temperature.

    .. math::
        Y = A + B\tau^{0.35} + C\tau^{2/3} + D\tau + E\tau^{4/3}

        \tau = 1 - \frac{T}{T_c}

    Parameters
    ----------
    T : float
        Temperature, [K]
    Tc : float
        Critical temperature, [K]
    A-E : float
        Parameter for the equation; chemical and property specific [-]
    order : int, optional
        Order of the calculation. 0 for the calculation of the result itself;
        for 1, the first derivative of the property is returned, for
        -1, the indefinite integral of the property with respect to temperature
        is returned; and for -1j, the indefinite integral of the property
        divided by temperature with respect to temperature is returned. No 
        other integrals or derivatives are implemented, and an exception will 
        be raised if any other order is given.

    Returns
    -------
    Y : float
        Property [constant-specific; if order == 1, property/K; if order == -1,
                  property*K; if order == -1j, unchanged from default]

    Notes
    -----
    The derivative with respect to T and integral with respect to T are 
    computed as follows. The integral divided by T with respect to T has an
    extremely complicated (but still elementary) integral which can be read 
    from the source. It was computed with Rubi; the other expressions can 
    readily be obtained with SymPy.

    .. math::
        \frac{d Y}{dT} = - \frac{7 B}{20 T_c \left(- \frac{T}{T_c} + 1\right)^{
        \frac{13}{20}}} - \frac{2 C}{3 T_c \sqrt[3]{- \frac{T}{T_c} + 1}} 
        - \frac{D}{T_c} - \frac{4 E}{3 T_c} \sqrt[3]{- \frac{T}{T_c} + 1}

    .. math::
        \int Y dT = A T - \frac{20 B}{27} T_c \left(- \frac{T}{T_c} + 1\right)^{
        \frac{27}{20}} - \frac{3 C}{5} T_c \left(- \frac{T}{T_c} + 1\right)^{
        \frac{5}{3}} + D \left(- \frac{T^{2}}{2 T_c} + T\right) - \frac{3 E}{7} 
        T_c \left(- \frac{T}{T_c} + 1\right)^{\frac{7}{3}}
                
    Examples
    --------
    Water liquid molar density; DIPPR coefficients normally in kmol/m^3.

    >>> EQ116(300., 647.096, 17.863, 58.606, -95.396, 213.89, -141.26)
    55.17615446406527

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    if order == 0:
        tau = 1-T/Tc
        return A + B*tau**0.35 + C*tau**(2/3.) + D*tau + E*tau**(4/3.)
    elif order == 1:
        return (-7*B/(20*Tc*(-T/Tc + 1)**(13/20)) 
                - 2*C/(3*Tc*(-T/Tc + 1)**(1/3)) 
                - D/Tc - 4*E*(-T/Tc + 1)**(1/3)/(3*Tc))
    elif order == -1:
        return (A*T - 20*B*Tc*(-T/Tc + 1)**(27/20)/27 
                - 3*C*Tc*(-T/Tc + 1)**(5/3)/5 + D*(-T**2/(2*Tc) + T)
                - 3*E*Tc*(-T/Tc + 1)**(7/3)/7)
    elif order == -1j:
        # 3x increase in speed - cse via sympy
        x0 = log(T)
        x1 = 0.5*x0
        x2 = 1/Tc
        x3 = T*x2
        x4 = -x3 + 1
        x5 = 1.5*C
        x6 = x4**0.333333333333333
        x7 = 2*B
        x8 = x4**0.05
        x9 = log(-x6 + 1)
        x10 = sqrt(3)
        x11 = x10*atan(x10*(2*x6 + 1)/3)
        x12 = sqrt(5)
        x13 = 0.5*x12
        x14 = x13 + 0.5
        x15 = B*x14
        x16 = sqrt(x13 + 2.5)
        x17 = 2*x8
        x18 = -x17
        x19 = -x13
        x20 = x19 + 0.5
        x21 = B*x20
        x22 = sqrt(x19 + 2.5)
        x23 = B*x16
        x24 = 0.5*sqrt(0.1*x12 + 0.5)
        x25 = x12 + 1
        x26 = 4*x8
        x27 = -x26
        x28 = sqrt(10)*B/sqrt(x12 + 5)
        x29 = 2*x12
        x30 = sqrt(x29 + 10)
        x31 = 1/x30
        x32 = -x12 + 1
        x33 = 0.5*B*x22
        x34 = -x2*(T - Tc)
        x35 = 2*x34**0.1
        x36 = x35 + 2
        x37 = x34**0.05
        x38 = x30*x37
        x39 = 0.5*B*x16
        x40 = x37*sqrt(-x29 + 10)
        x41 = 0.25*x12
        x42 = B*(-x41 + 0.25)
        x43 = x12*x37
        x44 = x35 + x37 + 2
        x45 = B*(x41 + 0.25)
        x46 = -x43
        x47 = x35 - x37 + 2
        return A*x0 + 2.85714285714286*B*x4**0.35 - C*x1 + C*x11 + D*x0 - D*x3 - E*x1 - E*x11 + 0.75*E*x4**1.33333333333333 + 3*E*x6 + 1.5*E*x9 - x15*atan(x14*(x16 + x17)) + x15*atan(x14*(x16 + x18)) - x21*atan(x20*(x17 + x22)) + x21*atan(x20*(x18 + x22)) + x23*atan(x24*(x25 + x26)) - x23*atan(x24*(x25 + x27)) - x28*atan(x31*(x26 + x32)) + x28*atan(x31*(x27 + x32)) - x33*log(x36 - x38) + x33*log(x36 + x38) + x39*log(x36 - x40) - x39*log(x36 + x40) + x4**0.666666666666667*x5 - x42*log(x43 + x44) + x42*log(x46 + x47) + x45*log(x43 + x47) - x45*log(x44 + x46) + x5*x9 + x7*atan(x8) - x7*atanh(x8)
    else:
        raise Exception(order_not_found_msg)