def Tm_depression_eutectic(Tm, Hm, x=None, M=None, MW=None):
    r'''Returns the freezing point depression caused by a solute in a solvent.
    Can use either the mole fraction of the solute or its molality and the
    molecular weight of the solvent. Assumes ideal system behavior.

    .. math::
        \Delta T_m = \frac{R T_m^2 x}{\Delta H_m}

        \Delta T_m = \frac{R T_m^2 (MW) M}{1000 \Delta H_m}

    Parameters
    ----------
    Tm : float
        Melting temperature of the solute [K]
    Hm : float
        Heat of melting at the melting temperature of the solute [J/mol]
    x : float, optional
        Mole fraction of the solute [-]
    M : float, optional
        Molality [mol/kg]
    MW: float, optional
        Molecular weight of the solvent [g/mol]

    Returns
    -------
    dTm : float
        Freezing point depression [K]

    Notes
    -----
    MW is the molecular weight of the solvent. M is the molality of the solute.

    Examples
    --------
    From [1]_, matching example.

    >>> Tm_depression_eutectic(353.35, 19110, .02)
    1.0864594900639515

    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    '''
    if x:
        dTm = R*Tm**2*x/Hm
    elif M and MW:
        MW = MW/1000. #g/mol to kg/mol
        dTm = R*Tm**2*MW*M/Hm
    else:
        raise Exception('Either molality or mole fraction of the solute must be specified; MW of the solvent is required also if molality is provided')
    return dTm