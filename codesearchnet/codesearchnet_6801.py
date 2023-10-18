def solubility_parameter(T=298.15, Hvapm=None, Vml=None,
                         CASRN='', AvailableMethods=False, Method=None):
    r'''This function handles the calculation of a chemical's solubility
    parameter. Calculation is a function of temperature, but is not always
    presented as such. No lookup values are available; either `Hvapm`, `Vml`,
    and `T` are provided or the calculation cannot be performed.

    .. math::
        \delta = \sqrt{\frac{\Delta H_{vap} - RT}{V_m}}

    Parameters
    ----------
    T : float
        Temperature of the fluid [k]
    Hvapm : float
        Heat of vaporization [J/mol/K]
    Vml : float
        Specific volume of the liquid [m^3/mol]
    CASRN : str, optional
        CASRN of the fluid, not currently used [-]

    Returns
    -------
    delta : float
        Solubility parameter, [Pa^0.5]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain the solubility parameter
        with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        solubility_parameter_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        the solubility parameter for the desired chemical, and will return
        methods instead of the solubility parameter

    Notes
    -----
    Undefined past the critical point. For convenience, if Hvap is not defined,
    an error is not raised; None is returned instead. Also for convenience,
    if Hvapm is less than RT, None is returned to avoid taking the root of a
    negative number.

    This parameter is often given in units of cal/ml, which is 2045.48 times
    smaller than the value returned here.

    Examples
    --------
    Pentane at STP

    >>> solubility_parameter(T=298.2, Hvapm=26403.3, Vml=0.000116055)
    14357.681538173534

    References
    ----------
    .. [1] Barton, Allan F. M. CRC Handbook of Solubility Parameters and Other
       Cohesion Parameters, Second Edition. CRC Press, 1991.
    '''
    def list_methods():
        methods = []
        if T and Hvapm and Vml:
            methods.append(DEFINITION)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == DEFINITION:
        if (not Hvapm) or (not T) or (not Vml):
            delta = None
        else:
            if Hvapm < R*T or Vml < 0:  # Prevent taking the root of a negative number
                delta = None
            else:
                delta = ((Hvapm - R*T)/Vml)**0.5
    elif Method == NONE:
        delta = None
    else:
        raise Exception('Failure in in function')
    return delta