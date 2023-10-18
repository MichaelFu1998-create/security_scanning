def ppmv_to_mgm3(ppmv, MW, T=298.15, P=101325.):
    r'''Converts a concentration in ppmv to units of mg/m^3. Used in
    industrial toxicology.

    .. math::
        \frac{mg}{m^3} = \frac{ppmv\cdot P}{RT}\cdot \frac{MW}{1000}

    Parameters
    ----------
    ppmv : float
        Concentratoin of a component in a gas mixure [parts per million,
        volumetric]
    MW : float
        Molecular weight of the trace gas [g/mol]
    T : float, optional
        Temperature of the gas at which the ppmv is reported
    P : float, optional
        Pressure of the gas at which the ppmv is reported

    Returns
    -------
    mgm3 : float
        Concentration of a substance in an ideal gas mixture [mg/m^3]

    Notes
    -----
    The term P/(RT)/1000 converts to 0.040874 at STP. Its inverse is reported
    as 24.45 in [1]_.

    Examples
    --------
    >>> ppmv_to_mgm3(1, 40)
    1.6349623351068687

    References
    ----------
    .. [1] ACGIH. Industrial Ventilation: A Manual of Recommended Practice,
       23rd Edition. American Conference of Governmental and Industrial
       Hygenists, 2004.
    '''
    parts = ppmv*1E-6
    n = parts*P/(R*T)
    mgm3 = MW*n*1000  # mol toxin /m^3 * g/mol toxis * 1000 mg/g
    return mgm3