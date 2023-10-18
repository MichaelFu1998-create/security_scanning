def EQ102(T, A, B, C, D, order=0):
    r'''DIPPR Equation # 102. Used in calculating vapor viscosity, vapor
    thermal conductivity, and sometimes solid heat capacity. High values of B
    raise an OverflowError.
    All 4 parameters are required. C and D are often 0.

    .. math::
        Y = \frac{A\cdot T^B}{1 + \frac{C}{T} + \frac{D}{T^2}}

    Parameters
    ----------
    T : float
        Temperature, [K]
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
    over T with respect to T are computed as follows. The first derivative is
    easily computed; the two integrals required Rubi to perform the integration.
    
    .. math::
        \frac{d Y}{dT} = \frac{A B T^{B}}{T \left(\frac{C}{T} + \frac{D}{T^{2}} 
        + 1\right)} + \frac{A T^{B} \left(\frac{C}{T^{2}} + \frac{2 D}{T^{3}}
        \right)}{\left(\frac{C}{T} + \frac{D}{T^{2}} + 1\right)^{2}}
        
    .. math::
        \int Y dT = - \frac{2 A T^{B + 3} \operatorname{hyp2f1}{\left (1,B + 3,
        B + 4,- \frac{2 T}{C - \sqrt{C^{2} - 4 D}} \right )}}{\left(B + 3\right) 
        \left(C + \sqrt{C^{2} - 4 D}\right) \sqrt{C^{2} - 4 D}} + \frac{2 A 
        T^{B + 3} \operatorname{hyp2f1}{\left (1,B + 3,B + 4,- \frac{2 T}{C 
        + \sqrt{C^{2} - 4 D}} \right )}}{\left(B + 3\right) \left(C 
        - \sqrt{C^{2} - 4 D}\right) \sqrt{C^{2} - 4 D}}
        
    .. math::
        \int \frac{Y}{T} dT = - \frac{2 A T^{B + 2} \operatorname{hyp2f1}{\left
        (1,B + 2,B + 3,- \frac{2 T}{C + \sqrt{C^{2} - 4 D}} \right )}}{\left(B 
        + 2\right) \left(C + \sqrt{C^{2} - 4 D}\right) \sqrt{C^{2} - 4 D}}
        + \frac{2 A T^{B + 2} \operatorname{hyp2f1}{\left (1,B + 2,B + 3,
        - \frac{2 T}{C - \sqrt{C^{2} - 4 D}} \right )}}{\left(B + 2\right) 
        \left(C - \sqrt{C^{2} - 4 D}\right) \sqrt{C^{2} - 4 D}}
        
    Examples
    --------
    Water vapor viscosity; DIPPR coefficients normally listed in Pa*s.

    >>> EQ102(300, 1.7096E-8, 1.1146, 0, 0)
    9.860384711890639e-06

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    if order == 0:
        return A*T**B/(1. + C/T + D/(T*T))
    elif order == 1:
        return (A*B*T**B/(T*(C/T + D/T**2 + 1)) 
                + A*T**B*(C/T**2 + 2*D/T**3)/(C/T + D/T**2 + 1)**2)
    elif order == -1:
        # imaginary part is 0
        return (2*A*T**(3+B)*hyp2f1(1, 3+B, 4+B, -2*T/(C - csqrt(C*C 
                - 4*D)))/((3+B)*(C - csqrt(C*C-4*D))*csqrt(C*C-4*D))
                -2*A*T**(3+B)*hyp2f1(1, 3+B, 4+B, -2*T/(C + csqrt(C*C - 4*D)))/(
                (3+B)*(C + csqrt(C*C-4*D))*csqrt(C*C-4*D))).real
    elif order == -1j:
        return (2*A*T**(2+B)*hyp2f1(1, 2+B, 3+B, -2*T/(C - csqrt(C*C - 4*D)))/(
                (2+B)*(C - csqrt(C*C-4*D))*csqrt(C*C-4*D)) -2*A*T**(2+B)*hyp2f1(
                1, 2+B, 3+B, -2*T/(C + csqrt(C*C - 4*D)))/((2+B)*(C + csqrt(
                C*C-4*D))*csqrt(C*C-4*D))).real
    else:
        raise Exception(order_not_found_msg)