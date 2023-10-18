def dilute_ionic_conductivity(ionic_conductivities, zs, rhom):
    r'''This function handles the calculation of the electrical conductivity of 
    a dilute electrolytic aqueous solution. Requires the mole fractions of 
    each ion, the molar density of the whole mixture, and ionic conductivity 
    coefficients for each ion.
    
    .. math::
        \lambda = \sum_i \lambda_i^\circ z_i \rho_m
    
    Parameters
    ----------
    ionic_conductivities : list[float]
        Ionic conductivity coefficients of each ion in the mixture [m^2*S/mol]
    zs : list[float]
        Mole fractions of each ion in the mixture, [-]
    rhom : float
        Overall molar density of the solution, [mol/m^3]

    Returns
    -------
    kappa : float
        Electrical conductivity of the fluid, [S/m]

    Notes
    -----
    The ionic conductivity coefficients should not be `equivalent` coefficients; 
    for example, 0.0053 m^2*S/mol is the equivalent conductivity coefficient of
    Mg+2, but this method expects twice its value - 0.0106. Both are reported
    commonly in literature.
    
    Water can be included in this caclulation by specifying a coefficient of
    0. The conductivity of any electrolyte eclipses its own conductivity by 
    many orders of magnitude. Any other solvents present will affect the
    conductivity extensively and there are few good methods to predict this 
    effect.

    Examples
    --------
    Complex mixture of electrolytes ['Cl-', 'HCO3-', 'SO4-2', 'Na+', 'K+', 
    'Ca+2', 'Mg+2']:
    
    >>> ionic_conductivities = [0.00764, 0.00445, 0.016, 0.00501, 0.00735, 0.0119, 0.01061]
    >>> zs = [0.03104, 0.00039, 0.00022, 0.02413, 0.0009, 0.0024, 0.00103]
    >>> dilute_ionic_conductivity(ionic_conductivities=ionic_conductivities, zs=zs, rhom=53865.9)
    22.05246783663

    References
    ----------
    .. [1] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
    '''
    return sum([ci*(zi*rhom) for zi, ci in zip(zs, ionic_conductivities)])