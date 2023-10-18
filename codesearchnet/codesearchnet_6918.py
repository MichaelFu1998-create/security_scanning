def EQ114(T, Tc, A, B, C, D, order=0):
    r'''DIPPR Equation #114. Rarely used, normally as an alternate liquid
    heat capacity expression. All 4 parameters are required, as well as
    critical temperature.

    .. math::
        Y = \frac{A^2}{\tau} + B - 2AC\tau - AD\tau^2 - \frac{1}{3}C^2\tau^3
        - \frac{1}{2}CD\tau^4 - \frac{1}{5}D^2\tau^5

        \tau = 1 - \frac{T}{Tc}

    Parameters
    ----------
    T : float
        Temperature, [K]
    Tc : float
        Critical temperature, [K]
    A-D : float
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
    The derivative with respect to T, integral with respect to T, and integral
    over T with respect to T are computed as follows. All expressions can be
    obtained with SymPy readily.
    
    .. math::
        \frac{d Y}{dT} = \frac{A^{2}}{T_{c} \left(- \frac{T}{T_{c}} 
        + 1\right)^{2}} + \frac{2 A}{T_{c}} C + \frac{2 A}{T_{c}} D \left(
        - \frac{T}{T_{c}} + 1\right) + \frac{C^{2}}{T_{c}} \left(
        - \frac{T}{T_{c}} + 1\right)^{2} + \frac{2 C}{T_{c}} D \left(
        - \frac{T}{T_{c}} + 1\right)^{3} + \frac{D^{2}}{T_{c}} \left(
        - \frac{T}{T_{c}} + 1\right)^{4}
        
    .. math::
        \int Y dT = - A^{2} T_{c} \log{\left (T - T_{c} \right )} + \frac{D^{2}
        T^{6}}{30 T_{c}^{5}} - \frac{T^{5}}{10 T_{c}^{4}} \left(C D + 2 D^{2}
        \right) + \frac{T^{4}}{12 T_{c}^{3}} \left(C^{2} + 6 C D + 6 D^{2}
        \right) - \frac{T^{3}}{3 T_{c}^{2}} \left(A D + C^{2} + 3 C D 
        + 2 D^{2}\right) + \frac{T^{2}}{2 T_{c}} \left(2 A C + 2 A D + C^{2} 
        + 2 C D + D^{2}\right) + T \left(- 2 A C - A D + B - \frac{C^{2}}{3} 
        - \frac{C D}{2} - \frac{D^{2}}{5}\right)
        
    .. math::
        \int \frac{Y}{T} dT = - A^{2} \log{\left (T + \frac{- 60 A^{2} T_{c}
        + 60 A C T_{c} + 30 A D T_{c} - 30 B T_{c} + 10 C^{2} T_{c}
        + 15 C D T_{c} + 6 D^{2} T_{c}}{60 A^{2} - 60 A C - 30 A D + 30 B 
        - 10 C^{2} - 15 C D - 6 D^{2}} \right )} + \frac{D^{2} T^{5}}
        {25 T_{c}^{5}} - \frac{T^{4}}{8 T_{c}^{4}} \left(C D + 2 D^{2}
        \right) + \frac{T^{3}}{9 T_{c}^{3}} \left(C^{2} + 6 C D + 6 D^{2}
        \right) - \frac{T^{2}}{2 T_{c}^{2}} \left(A D + C^{2} + 3 C D
        + 2 D^{2}\right) + \frac{T}{T_{c}} \left(2 A C + 2 A D + C^{2} 
        + 2 C D + D^{2}\right) + \frac{1}{30} \left(30 A^{2} - 60 A C 
        - 30 A D + 30 B - 10 C^{2} - 15 C D - 6 D^{2}\right) \log{\left 
        (T + \frac{1}{60 A^{2} - 60 A C - 30 A D + 30 B - 10 C^{2} - 15 C D
        - 6 D^{2}} \left(- 30 A^{2} T_{c} + 60 A C T_{c} + 30 A D T_{c} 
        - 30 B T_{c} + 10 C^{2} T_{c} + 15 C D T_{c} + 6 D^{2} T_{c}
        + T_{c} \left(30 A^{2} - 60 A C - 30 A D + 30 B - 10 C^{2} - 15 C D
        - 6 D^{2}\right)\right) \right )}

    Strictly speaking, the integral over T has an imaginary component, but
    only the real component is relevant and the complex part discarded.

    Examples
    --------
    Hydrogen liquid heat capacity; DIPPR coefficients normally in J/kmol/K.

    >>> EQ114(20, 33.19, 66.653, 6765.9, -123.63, 478.27)
    19423.948911676463

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    if order == 0:
        t = 1.-T/Tc
        return (A**2./t + B - 2.*A*C*t - A*D*t**2. - C**2.*t**3./3. 
                - C*D*t**4./2. - D**2*t**5./5.)
    elif order == 1:
        return (A**2/(Tc*(-T/Tc + 1)**2) + 2*A*C/Tc + 2*A*D*(-T/Tc + 1)/Tc 
                + C**2*(-T/Tc + 1)**2/Tc + 2*C*D*(-T/Tc + 1)**3/Tc 
                + D**2*(-T/Tc + 1)**4/Tc)
    elif order == -1:
        return (-A**2*Tc*clog(T - Tc).real + D**2*T**6/(30*Tc**5) 
                - T**5*(C*D + 2*D**2)/(10*Tc**4) 
                + T**4*(C**2 + 6*C*D + 6*D**2)/(12*Tc**3) - T**3*(A*D + C**2 
                + 3*C*D + 2*D**2)/(3*Tc**2) + T**2*(2*A*C + 2*A*D + C**2 + 2*C*D 
                + D**2)/(2*Tc) + T*(-2*A*C - A*D + B - C**2/3 - C*D/2 - D**2/5))
    elif order == -1j:
        return (-A**2*clog(T + (-60*A**2*Tc + 60*A*C*Tc + 30*A*D*Tc - 30*B*Tc 
                + 10*C**2*Tc + 15*C*D*Tc + 6*D**2*Tc)/(60*A**2 - 60*A*C 
                - 30*A*D + 30*B - 10*C**2 - 15*C*D - 6*D**2)).real 
                + D**2*T**5/(25*Tc**5) - T**4*(C*D + 2*D**2)/(8*Tc**4) 
                + T**3*(C**2 + 6*C*D + 6*D**2)/(9*Tc**3) - T**2*(A*D + C**2
                + 3*C*D + 2*D**2)/(2*Tc**2) + T*(2*A*C + 2*A*D + C**2 + 2*C*D
                + D**2)/Tc + (30*A**2 - 60*A*C - 30*A*D + 30*B - 10*C**2
                - 15*C*D - 6*D**2)*clog(T + (-30*A**2*Tc + 60*A*C*Tc 
                + 30*A*D*Tc - 30*B*Tc + 10*C**2*Tc + 15*C*D*Tc + 6*D**2*Tc 
                + Tc*(30*A**2 - 60*A*C - 30*A*D + 30*B - 10*C**2 - 15*C*D 
                - 6*D**2))/(60*A**2 - 60*A*C - 30*A*D + 30*B - 10*C**2 
                - 15*C*D - 6*D**2)).real/30)
    else:
        raise Exception(order_not_found_msg)