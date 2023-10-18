def CoolProp_T_dependent_property(T, CASRN, prop, phase):
    r'''Calculates a property of a chemical in either the liquid or gas phase
    as a function of temperature only. This means that the property is
    either at 1 atm or along the saturation curve.

    Parameters
    ----------
    T : float
        Temperature of the fluid [K]
    CASRN : str
        CAS number of the fluid
    prop : str
        CoolProp string shortcut for desired property
    phase : str
        Either 'l' or 'g' for liquid or gas properties respectively

    Returns
    -------
    prop : float
        Desired chemical property, [units]

    Notes
    -----
    For liquids above their boiling point, the liquid property is found on the
    saturation line (at higher pressures). Under their boiling point, the
    property is calculated at 1 atm.

    No liquid calculations are permitted above the critical temperature.

    For gases under the chemical's boiling point, the gas property is found
    on the saturation line (at sub-atmospheric pressures). Above the boiling
    point, the property is calculated at 1 atm.

    An exception is raised if the desired CAS is not supported, or if CoolProp
    is not available.

    The list of strings acceptable as an input for property types is:
    http://www.coolprop.org/coolprop/HighLevelAPI.html#table-of-string-inputs-to-propssi-function

    Examples
    --------
    Water at STP according to IAPWS-95

    >>> CoolProp_T_dependent_property(298.15, '7732-18-5', 'D', 'l')
    997.047636760347

    References
    ----------
    .. [1] Bell, Ian H., Jorrit Wronski, Sylvain Quoilin, and Vincent Lemort.
       "Pure and Pseudo-Pure Fluid Thermophysical Property Evaluation and the
       Open-Source Thermophysical Property Library CoolProp." Industrial &
       Engineering Chemistry Research 53, no. 6 (February 12, 2014):
       2498-2508. doi:10.1021/ie4033999. http://www.coolprop.org/
    '''
    if not has_CoolProp:  # pragma: no cover
        raise Exception('CoolProp library is not installed')
    if CASRN not in coolprop_dict:
        raise Exception('CASRN not in list of supported fluids')
    Tc = coolprop_fluids[CASRN].Tc
    T = float(T) # Do not allow custom objects here
    if phase == 'l':
        if T > Tc:
            raise Exception('For liquid properties, must be under the critical temperature.')
        if PhaseSI('T', T, 'P', 101325, CASRN) in [u'liquid', u'supercritical_liquid']:
            return PropsSI(prop, 'T', T, 'P', 101325, CASRN)
        else:
            return PropsSI(prop, 'T', T, 'Q', 0, CASRN)
    elif phase == 'g':
        if PhaseSI('T', T, 'P', 101325, CASRN) == 'gas':
            return PropsSI(prop, 'T', T, 'P', 101325, CASRN)
        else:
            if T < Tc:
                return PropsSI(prop, 'T', T, 'Q', 1, CASRN)
            else:
                # catch supercritical_gas and friends
                return PropsSI(prop, 'T', T, 'P', 101325, CASRN)
    else:
        raise Exception('Error in CoolProp property function')