def phase_select_property(phase=None, s=None, l=None, g=None, V_over_F=None):
    r'''Determines which phase's property should be set as a default, given
    the phase a chemical is, and the property values of various phases. For the
    case of liquid-gas phase, returns None. If the property is not available
    for the current phase, or if the current phase is not known, returns None.

    Parameters
    ----------
    phase : str
        One of {'s', 'l', 'g', 'two-phase'}
    s : float
        Solid-phase property
    l : float
        Liquid-phase property
    g : float
        Gas-phase property
    V_over_F : float
        Vapor phase fraction

    Returns
    -------
    prop : float
        The selected/calculated property for the relevant phase

    Notes
    -----
    Could calculate mole-fraction weighted properties for the two phase regime.
    Could also implement equilibria with solid phases.

    Examples
    --------
    >>> phase_select_property(phase='g', l=1560.14, g=3312.)
    3312.0
    '''
    if phase == 's':
        return s
    elif phase == 'l':
        return l
    elif phase == 'g':
        return g
    elif phase == 'two-phase':
        return None  #TODO: all two-phase properties?
    elif phase is None:
        return None
    else:
        raise Exception('Property not recognized')