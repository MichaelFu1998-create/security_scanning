def UNIFAC_RQ(groups, subgroup_data=None):
    r'''Calculates UNIFAC parameters R and Q for a chemical, given a dictionary
    of its groups, as shown in [1]_. Most UNIFAC methods use the same subgroup
    values; however, a dictionary of `UNIFAC_subgroup` instances may be 
    specified as an optional second parameter.

    .. math::
        r_i = \sum_{k=1}^{n} \nu_k R_k 
        
        q_i = \sum_{k=1}^{n}\nu_k Q_k

    Parameters
    ----------
    groups : dict[count]
        Dictionary of numeric subgroup IDs : their counts
    subgroup_data : None or dict[UNIFAC_subgroup]
        Optional replacement for standard subgroups; leave as None to use the
        original UNIFAC subgroup r and q values.

    Returns
    -------
    R : float
        R UNIFAC parameter (normalized Van der Waals Volume)  [-]
    Q : float
        Q UNIFAC parameter (normalized Van der Waals Area)  [-]

    Notes
    -----
    These parameters have some predictive value for other chemical properties.

    Examples
    --------
    Hexane
    
    >>> UNIFAC_RQ({1:2, 2:4})
    (4.4998000000000005, 3.856)
    
    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    '''
    if subgroup_data is not None:
        subgroups = subgroup_data
    else:
        subgroups = UFSG
    ri = 0.
    qi = 0.
    for group, count in groups.items():
        ri += subgroups[group].R*count
        qi += subgroups[group].Q*count
    return ri, qi