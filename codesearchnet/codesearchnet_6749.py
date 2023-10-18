def TWU_a_alpha_common(T, Tc, omega, a, full=True, quick=True, method='PR'):
    r'''Function to calculate `a_alpha` and optionally its first and second
    derivatives for the TWUPR or TWUSRK EOS. Returns 'a_alpha', and 
    optionally 'da_alpha_dT' and 'd2a_alpha_dT2'.
    Used by `TWUPR` and `TWUSRK`; has little purpose on its own.
    See either class for the correct reference, and examples of using the EOS.

    Parameters
    ----------
    T : float
        Temperature, [K]
    Tc : float
        Critical temperature, [K]
    omega : float
        Acentric factor, [-]
    a : float
        Coefficient calculated by EOS-specific method, [J^2/mol^2/Pa]
    full : float
        Whether or not to return its first and second derivatives
    quick : bool, optional
        Whether to use a SymPy cse-derived expression (3x faster) or 
        individual formulas
    method : str
        Either 'PR' or 'SRK'
        
    Notes
    -----
    The derivatives are somewhat long and are not described here for 
    brevity; they are obtainable from the following SymPy expression.
    
    >>> from sympy import *
    >>> T, Tc, omega, N1, N0, M1, M0, L1, L0 = symbols('T, Tc, omega, N1, N0, M1, M0, L1, L0')
    >>> Tr = T/Tc
    >>> alpha0 = Tr**(N0*(M0-1))*exp(L0*(1-Tr**(N0*M0)))
    >>> alpha1 = Tr**(N1*(M1-1))*exp(L1*(1-Tr**(N1*M1)))
    >>> alpha = alpha0 + omega*(alpha1-alpha0)
    >>> # diff(alpha, T)
    >>> # diff(alpha, T, T)
    '''
    Tr = T/Tc
    if method == 'PR':
        if Tr < 1:
            L0, M0, N0 = 0.125283, 0.911807, 1.948150
            L1, M1, N1 = 0.511614, 0.784054, 2.812520
        else:
            L0, M0, N0 = 0.401219, 4.963070, -0.2
            L1, M1, N1 = 0.024955, 1.248089, -8.  
    elif method == 'SRK':
        if Tr < 1:
            L0, M0, N0 = 0.141599, 0.919422, 2.496441
            L1, M1, N1 = 0.500315, 0.799457, 3.291790
        else:
            L0, M0, N0 = 0.441411, 6.500018, -0.20
            L1, M1, N1 = 0.032580,  1.289098, -8.0
    else:
        raise Exception('Only `PR` and `SRK` are accepted as method')
    
    if not full:
        alpha0 = Tr**(N0*(M0-1.))*exp(L0*(1.-Tr**(N0*M0)))
        alpha1 = Tr**(N1*(M1-1.))*exp(L1*(1.-Tr**(N1*M1)))
        alpha = alpha0 + omega*(alpha1 - alpha0)
        return a*alpha
    else:
        if quick:
            x0 = T/Tc
            x1 = M0 - 1
            x2 = N0*x1
            x3 = x0**x2
            x4 = M0*N0
            x5 = x0**x4
            x6 = exp(-L0*(x5 - 1.))
            x7 = x3*x6
            x8 = M1 - 1.
            x9 = N1*x8
            x10 = x0**x9
            x11 = M1*N1
            x12 = x0**x11
            x13 = x2*x7
            x14 = L0*M0*N0*x3*x5*x6
            x15 = x13 - x14
            x16 = exp(-L1*(x12 - 1))
            x17 = -L1*M1*N1*x10*x12*x16 + x10*x16*x9 - x13 + x14
            x18 = N0*N0
            x19 = x18*x3*x6
            x20 = x1**2*x19
            x21 = M0**2
            x22 = L0*x18*x3*x5*x6
            x23 = x21*x22
            x24 = 2*M0*x1*x22
            x25 = L0**2*x0**(2*x4)*x19*x21
            x26 = N1**2
            x27 = x10*x16*x26
            x28 = M1**2
            x29 = L1*x10*x12*x16*x26
            a_alpha = a*(-omega*(-x10*exp(L1*(-x12 + 1)) + x3*exp(L0*(-x5 + 1))) + x7)
            da_alpha_dT = a*(omega*x17 + x15)/T
            d2a_alpha_dT2 = a*(-(omega*(-L1**2*x0**(2.*x11)*x27*x28 + 2.*M1*x29*x8 + x17 + x20 - x23 - x24 + x25 - x27*x8**2 + x28*x29) + x15 - x20 + x23 + x24 - x25)/T**2)
        else:
            a_alpha = TWU_a_alpha_common(T=T, Tc=Tc, omega=omega, a=a, full=False, quick=quick, method=method)
            da_alpha_dT = a*(-L0*M0*N0*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(L0*(-(T/Tc)**(M0*N0) + 1))/T + N0*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)*exp(L0*(-(T/Tc)**(M0*N0) + 1))/T + omega*(L0*M0*N0*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(L0*(-(T/Tc)**(M0*N0) + 1))/T - L1*M1*N1*(T/Tc)**(M1*N1)*(T/Tc)**(N1*(M1 - 1))*exp(L1*(-(T/Tc)**(M1*N1) + 1))/T - N0*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)*exp(L0*(-(T/Tc)**(M0*N0) + 1))/T + N1*(T/Tc)**(N1*(M1 - 1))*(M1 - 1)*exp(L1*(-(T/Tc)**(M1*N1) + 1))/T))
            d2a_alpha_dT2 = a*((L0**2*M0**2*N0**2*(T/Tc)**(2*M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(-L0*((T/Tc)**(M0*N0) - 1)) - L0*M0**2*N0**2*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(-L0*((T/Tc)**(M0*N0) - 1)) - 2*L0*M0*N0**2*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)*exp(-L0*((T/Tc)**(M0*N0) - 1)) + L0*M0*N0*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(-L0*((T/Tc)**(M0*N0) - 1)) + N0**2*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)**2*exp(-L0*((T/Tc)**(M0*N0) - 1)) - N0*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)*exp(-L0*((T/Tc)**(M0*N0) - 1)) - omega*(L0**2*M0**2*N0**2*(T/Tc)**(2*M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(-L0*((T/Tc)**(M0*N0) - 1)) - L0*M0**2*N0**2*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(-L0*((T/Tc)**(M0*N0) - 1)) - 2*L0*M0*N0**2*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)*exp(-L0*((T/Tc)**(M0*N0) - 1)) + L0*M0*N0*(T/Tc)**(M0*N0)*(T/Tc)**(N0*(M0 - 1))*exp(-L0*((T/Tc)**(M0*N0) - 1)) - L1**2*M1**2*N1**2*(T/Tc)**(2*M1*N1)*(T/Tc)**(N1*(M1 - 1))*exp(-L1*((T/Tc)**(M1*N1) - 1)) + L1*M1**2*N1**2*(T/Tc)**(M1*N1)*(T/Tc)**(N1*(M1 - 1))*exp(-L1*((T/Tc)**(M1*N1) - 1)) + 2*L1*M1*N1**2*(T/Tc)**(M1*N1)*(T/Tc)**(N1*(M1 - 1))*(M1 - 1)*exp(-L1*((T/Tc)**(M1*N1) - 1)) - L1*M1*N1*(T/Tc)**(M1*N1)*(T/Tc)**(N1*(M1 - 1))*exp(-L1*((T/Tc)**(M1*N1) - 1)) + N0**2*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)**2*exp(-L0*((T/Tc)**(M0*N0) - 1)) - N0*(T/Tc)**(N0*(M0 - 1))*(M0 - 1)*exp(-L0*((T/Tc)**(M0*N0) - 1)) - N1**2*(T/Tc)**(N1*(M1 - 1))*(M1 - 1)**2*exp(-L1*((T/Tc)**(M1*N1) - 1)) + N1*(T/Tc)**(N1*(M1 - 1))*(M1 - 1)*exp(-L1*((T/Tc)**(M1*N1) - 1))))/T**2)
        return a_alpha, da_alpha_dT, d2a_alpha_dT2