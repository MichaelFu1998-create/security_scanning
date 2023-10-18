def EQ107(T, A=0, B=0, C=0, D=0, E=0, order=0):
    r'''DIPPR Equation #107. Often used in calculating ideal-gas heat capacity.
    All 5 parameters are required.
    Also called the Aly-Lee equation.

    .. math::
        Y = A + B\left[\frac{C/T}{\sinh(C/T)}\right]^2 + D\left[\frac{E/T}{
        \cosh(E/T)}\right]^2

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
    over T with respect to T are computed as follows. The derivative is 
    obtained via SymPy; the integrals from Wolfram Alpha.
    
    .. math::
        \frac{d Y}{dT} = \frac{2 B C^{3} \cosh{\left (\frac{C}{T} \right )}}
        {T^{4} \sinh^{3}{\left (\frac{C}{T} \right )}} - \frac{2 B C^{2}}{T^{3}
        \sinh^{2}{\left (\frac{C}{T} \right )}} + \frac{2 D E^{3} \sinh{\left
        (\frac{E}{T} \right )}}{T^{4} \cosh^{3}{\left (\frac{E}{T} \right )}} 
        - \frac{2 D E^{2}}{T^{3} \cosh^{2}{\left (\frac{E}{T} \right )}}
        
    .. math::
        \int Y dT = A T + \frac{B C}{\tanh{\left (\frac{C}{T} \right )}}
        - D E \tanh{\left (\frac{E}{T} \right )}
        
    .. math::
        \int \frac{Y}{T} dT = A \log{\left (T \right )} + \frac{B C}{T \tanh{
        \left (\frac{C}{T} \right )}} - B \log{\left (\sinh{\left (\frac{C}{T}
        \right )} \right )} - \frac{D E}{T} \tanh{\left (\frac{E}{T} \right )}
        + D \log{\left (\cosh{\left (\frac{E}{T} \right )} \right )}
        
    Examples
    --------
    Water ideal gas molar heat capacity; DIPPR coefficients normally in
    J/kmol/K

    >>> EQ107(300., 33363., 26790., 2610.5, 8896., 1169.)
    33585.90452768923

    References
    ----------
    .. [1] Design Institute for Physical Properties, 1996. DIPPR Project 801
       DIPPR/AIChE
    .. [2] Aly, Fouad A., and Lloyd L. Lee. "Self-Consistent Equations for
       Calculating the Ideal Gas Heat Capacity, Enthalpy, and Entropy." Fluid
       Phase Equilibria 6, no. 3 (January 1, 1981): 169-79.
       doi:10.1016/0378-3812(81)85002-9.
    '''
    if order == 0:
        return A + B*((C/T)/sinh(C/T))**2 + D*((E/T)/cosh(E/T))**2
    elif order == 1:
        return (2*B*C**3*cosh(C/T)/(T**4*sinh(C/T)**3) 
                - 2*B*C**2/(T**3*sinh(C/T)**2) 
                + 2*D*E**3*sinh(E/T)/(T**4*cosh(E/T)**3)
                - 2*D*E**2/(T**3*cosh(E/T)**2))
    elif order == -1:
        return A*T + B*C/tanh(C/T) - D*E*tanh(E/T)
    elif order == -1j:
        return (A*log(T) + B*C/tanh(C/T)/T - B*log(sinh(C/T)) 
                - D*E*tanh(E/T)/T + D*log(cosh(E/T)))
    else:
        raise Exception(order_not_found_msg)