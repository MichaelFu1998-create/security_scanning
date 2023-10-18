def mgm3_to_ppmv(mgm3, MW, T=298.15, P=101325.):
    r'''Converts a concentration in  mg/m^3 to units of ppmv. Used in
    industrial toxicology.

    .. math::
        ppmv = \frac{1000RT}{MW\cdot P} \cdot \frac{mg}{m^3}

    Parameters
    ----------
    mgm3 : float
        Concentration of a substance in an ideal gas mixture [mg/m^3]
    MW : float
        Molecular weight of the trace gas [g/mol]
    T : float, optional
        Temperature of the gas at which the ppmv is reported
    P : float, optional
        Pressure of the gas at which the ppmv is reported

    Returns
    -------
    ppmv : float
        Concentration of a component in a gas mixure [parts per million,
        volumetric]

    Notes
    -----
    The term P/(RT)/1000 converts to 0.040874 at STP. Its inverse is reported
    as 24.45 in [1]_.

    Examples
    --------
    >>> mgm3_to_ppmv(1.635, 40)
    1.0000230371625833

    References
    ----------
    .. [1] ACGIH. Industrial Ventilation: A Manual of Recommended Practice,
       23rd Edition. American Conference of Governmental and Industrial
       Hygenists, 2004.
    '''
    n = mgm3/MW/1000.
    parts = n*R*T/P
    ppm = parts/1E-6
    return ppm