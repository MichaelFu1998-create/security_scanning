def EQ100(T, A=0, B=0, C=0, D=0, E=0, F=0, G=0, order=0):
    r'''DIPPR Equation # 100. Used in calculating the molar heat capacities
    of liquids and solids, liquid thermal conductivity, and solid density.
    All parameters default to zero. As this is a straightforward polynomial,
    no restrictions on parameters apply. Note that high-order polynomials like
    this may need large numbers of decimal places to avoid unnecessary error.

    .. math::
        Y = A + BT + CT^2 + DT^3 + ET^4 + FT^5 + GT^6

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
    over T with respect to T are computed as follows. All derivatives and 
    integrals are easily computed with SymPy.
    
    .. math::
        \frac{d Y}{dT} = B + 2 C T + 3 D T^{2} + 4 E T^{3} + 5 F T^{4} 
        + 6 G T^{5}
        
    .. math::
        \int Y dT = A T + \frac{B T^{2}}{2} + \frac{C T^{3}}{3} + \frac{D 
        T^{4}}{4} + \frac{E T^{5}}{5} + \frac{F T^{6}}{6} + \frac{G T^{7}}{7}
        
    .. math::
        \int \frac{Y}{T} dT = A \log{\left (T \right )} + B T + \frac{C T^{2}}
        {2} + \frac{D T^{3}}{3} + \frac{E T^{4}}{4} + \frac{F T^{5}}{5} 
        + \frac{G T^{6}}{6}

    Examples
    --------
    Water liquid heat capacity; DIPPR coefficients normally listed in J/kmol/K.

    >>> EQ100(300, 276370., -2090.1, 8.125, -0.014116, 0.0000093701)
    75355.81000000003

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    '''
    if order == 0:
        return A + T*(B + T*(C + T*(D + T*(E + T*(F + G*T)))))
    elif order == 1:
        return B + T*(2*C + T*(3*D + T*(4*E + T*(5*F + 6*G*T))))
    elif order == -1:
        return T*(A + T*(B/2 + T*(C/3 + T*(D/4 + T*(E/5 + T*(F/6 + G*T/7))))))
    elif order == -1j:
        return A*log(T) + T*(B + T*(C/2 + T*(D/3 + T*(E/4 + T*(F/5 + G*T/6)))))
    else:
        raise Exception(order_not_found_msg)