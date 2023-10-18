def EQ104(T, A, B, C, D, E, order=0):
    r'''DIPPR Equation #104. Often used in calculating second virial
    coefficients of gases. All 5 parameters are required.
    C, D, and E are normally large values.

    .. math::
        Y = A + \frac{B}{T} + \frac{C}{T^3} + \frac{D}{T^8} + \frac{E}{T^9}

    Parameters
    ----------
    T : float
        Temperature, [K]
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
    The derivative with respect to T, integral with respect to T, and integral
    over T with respect to T are computed as follows. All expressions can be
    obtained with SymPy readily.
    
    .. math::
        \frac{d Y}{dT} = - \frac{B}{T^{2}} - \frac{3 C}{T^{4}} 
        - \frac{8 D}{T^{9}} - \frac{9 E}{T^{10}}
        
    .. math::
        \int Y dT = A T + B \log{\left (T \right )} - \frac{1}{56 T^{8}} 
        \left(28 C T^{6} + 8 D T + 7 E\right)
        
    .. math::
        \int \frac{Y}{T} dT = A \log{\left (T \right )} - \frac{1}{72 T^{9}} 
        \left(72 B T^{8} + 24 C T^{6} + 9 D T + 8 E\right)

    Examples
    --------
    Water second virial coefficient; DIPPR coefficients normally dimensionless.

    >>> EQ104(300, 0.02222, -26.38, -16750000, -3.894E19, 3.133E21)
    -1.1204179007265156

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    if order == 0:
        T2 = T*T
        return A + (B + (C + (D + E/T)/(T2*T2*T))/T2)/T
    elif order == 1:
        T2 = T*T
        T4 = T2*T2
        return (-B + (-3*C + (-8*D - 9*E/T)/(T4*T))/T2)/T2
    elif order == -1:
        return A*T + B*log(T) - (28*C*T**6 + 8*D*T + 7*E)/(56*T**8)
    elif order == -1j:
        return A*log(T) - (72*B*T**8 + 24*C*T**6 + 9*D*T + 8*E)/(72*T**9)
    else:
        raise Exception(order_not_found_msg)