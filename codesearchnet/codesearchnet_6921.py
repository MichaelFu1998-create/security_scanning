def EQ127(T, A, B, C, D, E, F, G, order=0):
    r'''DIPPR Equation #127. Rarely used, and then only in calculating
    ideal-gas heat capacity. All 7 parameters are required.

    .. math::
        Y = A+B\left[\frac{\left(\frac{C}{T}\right)^2\exp\left(\frac{C}{T}
        \right)}{\left(\exp\frac{C}{T}-1 \right)^2}\right]
        +D\left[\frac{\left(\frac{E}{T}\right)^2\exp\left(\frac{E}{T}\right)}
        {\left(\exp\frac{E}{T}-1 \right)^2}\right]
        +F\left[\frac{\left(\frac{G}{T}\right)^2\exp\left(\frac{G}{T}\right)}
        {\left(\exp\frac{G}{T}-1 \right)^2}\right]

    Parameters
    ----------
    T : float
        Temperature, [K]
    A-G : float
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
        \frac{d Y}{dT} = - \frac{B C^{3} e^{\frac{C}{T}}}{T^{4}
        \left(e^{\frac{C}{T}} - 1\right)^{2}} + \frac{2 B C^{3} 
        e^{\frac{2 C}{T}}}{T^{4} \left(e^{\frac{C}{T}} - 1\right)^{3}} 
        - \frac{2 B C^{2} e^{\frac{C}{T}}}{T^{3} \left(e^{\frac{C}{T}} 
        - 1\right)^{2}} - \frac{D E^{3} e^{\frac{E}{T}}}{T^{4} 
        \left(e^{\frac{E}{T}} - 1\right)^{2}} + \frac{2 D E^{3} 
        e^{\frac{2 E}{T}}}{T^{4} \left(e^{\frac{E}{T}} - 1\right)^{3}}
        - \frac{2 D E^{2} e^{\frac{E}{T}}}{T^{3} \left(e^{\frac{E}{T}} 
        - 1\right)^{2}} - \frac{F G^{3} e^{\frac{G}{T}}}{T^{4}
        \left(e^{\frac{G}{T}} - 1\right)^{2}} + \frac{2 F G^{3}
        e^{\frac{2 G}{T}}}{T^{4} \left(e^{\frac{G}{T}} - 1\right)^{3}}
        - \frac{2 F G^{2} e^{\frac{G}{T}}}{T^{3} \left(e^{\frac{G}{T}} 
        - 1\right)^{2}}
        
    .. math::
        \int Y dT = A T + \frac{B C^{2}}{C e^{\frac{C}{T}} - C} 
        + \frac{D E^{2}}{E e^{\frac{E}{T}} - E} 
        + \frac{F G^{2}}{G e^{\frac{G}{T}} - G}
        
    .. math::
        \int \frac{Y}{T} dT = A \log{\left (T \right )} + B C^{2} \left(
        \frac{1}{C T e^{\frac{C}{T}} - C T} + \frac{1}{C T} - \frac{1}{C^{2}} 
        \log{\left (e^{\frac{C}{T}} - 1 \right )}\right) + D E^{2} \left(
        \frac{1}{E T e^{\frac{E}{T}} - E T} + \frac{1}{E T} - \frac{1}{E^{2}} 
        \log{\left (e^{\frac{E}{T}} - 1 \right )}\right) + F G^{2} \left(
        \frac{1}{G T e^{\frac{G}{T}} - G T} + \frac{1}{G T} - \frac{1}{G^{2}} 
        \log{\left (e^{\frac{G}{T}} - 1 \right )}\right)
            
    Examples
    --------
    Ideal gas heat capacity of methanol; DIPPR coefficients normally in
    J/kmol/K

    >>> EQ127(20., 3.3258E4, 3.6199E4, 1.2057E3, 1.5373E7, 3.2122E3, -1.5318E7, 3.2122E3)
    33258.0

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    if order == 0:
        return (A+B*((C/T)**2*exp(C/T)/(exp(C/T) - 1)**2) + 
            D*((E/T)**2*exp(E/T)/(exp(E/T)-1)**2) + 
            F*((G/T)**2*exp(G/T)/(exp(G/T)-1)**2))
    elif order == 1:
        return (-B*C**3*exp(C/T)/(T**4*(exp(C/T) - 1)**2) 
                + 2*B*C**3*exp(2*C/T)/(T**4*(exp(C/T) - 1)**3) 
                - 2*B*C**2*exp(C/T)/(T**3*(exp(C/T) - 1)**2) 
                - D*E**3*exp(E/T)/(T**4*(exp(E/T) - 1)**2) 
                + 2*D*E**3*exp(2*E/T)/(T**4*(exp(E/T) - 1)**3) 
                - 2*D*E**2*exp(E/T)/(T**3*(exp(E/T) - 1)**2) 
                - F*G**3*exp(G/T)/(T**4*(exp(G/T) - 1)**2)
                + 2*F*G**3*exp(2*G/T)/(T**4*(exp(G/T) - 1)**3) 
                - 2*F*G**2*exp(G/T)/(T**3*(exp(G/T) - 1)**2))
    elif order == -1:
        return (A*T + B*C**2/(C*exp(C/T) - C) + D*E**2/(E*exp(E/T) - E)
                + F*G**2/(G*exp(G/T) - G))
    elif order == -1j:
        return (A*log(T) + B*C**2*(1/(C*T*exp(C/T) - C*T) + 1/(C*T)
                - log(exp(C/T) - 1)/C**2) + D*E**2*(1/(E*T*exp(E/T) - E*T) 
                + 1/(E*T) - log(exp(E/T) - 1)/E**2)
                + F*G**2*(1/(G*T*exp(G/T) - G*T) + 1/(G*T) - log(exp(G/T) 
                - 1)/G**2))
    else:
        raise Exception(order_not_found_msg)