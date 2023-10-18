def solubility_eutectic(T, Tm, Hm, Cpl=0, Cps=0, gamma=1):
    r'''Returns the maximum solubility of a solute in a solvent.

    .. math::
        \ln x_i^L \gamma_i^L = \frac{\Delta H_{m,i}}{RT}\left(
        1 - \frac{T}{T_{m,i}}\right) - \frac{\Delta C_{p,i}(T_{m,i}-T)}{RT}
        + \frac{\Delta C_{p,i}}{R}\ln\frac{T_m}{T}

        \Delta C_{p,i} = C_{p,i}^L - C_{p,i}^S

    Parameters
    ----------
    T : float
        Temperature of the system [K]
    Tm : float
        Melting temperature of the solute [K]
    Hm : float
        Heat of melting at the melting temperature of the solute [J/mol]
    Cpl : float, optional
        Molar heat capacity of the solute as a liquid [J/mol/K]
    Cpls: float, optional
        Molar heat capacity of the solute as a solid [J/mol/K]
    gamma : float, optional
        Activity coefficient of the solute as a liquid [-]

    Returns
    -------
    x : float
        Mole fraction of solute at maximum solubility [-]

    Notes
    -----
    gamma is of the solute in liquid phase

    Examples
    --------
    From [1]_, matching example

    >>> solubility_eutectic(T=260., Tm=278.68, Hm=9952., Cpl=0, Cps=0, gamma=3.0176)
    0.24340068761677464

    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    '''
    dCp = Cpl-Cps
    x = exp(- Hm/R/T*(1-T/Tm) + dCp*(Tm-T)/R/T - dCp/R*log(Tm/T))/gamma
    return x