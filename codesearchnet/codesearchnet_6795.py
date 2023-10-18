def Watson(T, Hvap_ref, T_Ref, Tc, exponent=0.38):
    '''
    Adjusts enthalpy of vaporization of enthalpy for another temperature, for one temperature.
    '''
    Tr = T/Tc
    Trefr = T_Ref/Tc
    H2 = Hvap_ref*((1-Tr)/(1-Trefr))**exponent
    return H2