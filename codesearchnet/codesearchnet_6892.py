def Mersmann_Kind_predictor(atoms, coeff=3.645, power=0.5, 
                            covalent_radii=rcovs_Mersmann_Kind):
    r'''Predicts the critical molar volume of a chemical based only on its
    atomic composition according to [1]_ and [2]_. This is a crude approach,
    but provides very reasonable
    estimates in practice. Optionally, the `coeff` used and the `power` in the
    fraction as well as the atomic contributions can be adjusted; this method
    is general and atomic contributions can be regressed to predict other
    properties with this routine.
    
    .. math::
        \frac{\left(\frac{V_c}{n_a N_A}\right)^{1/3}}{d_a}
        = \frac{3.645}{\left(\frac{r_a}{r_H}\right)^{1/2}}

        r_a = d_a/2
        
        d_a = 2 \frac{\sum_i (n_i r_i)}{n_a}
        
    In the above equations, :math:`n_i` is the number of atoms of species i in
    the molecule, :math:`r_i` is the covalent atomic radius of the atom, and 
    :math:`n_a` is the total number of atoms in the molecule.
    
    Parameters
    ----------
    atoms : dict
        Dictionary of atoms and their counts, [-]
    coeff : float, optional
        Coefficient used in the relationship, [m^2]
    power : float, optional
        Power applied to the relative atomic radius, [-]
    covalent_radii : dict or indexable, optional
        Object which can be indexed to atomic contrinbutions (by symbol), [-]

    Returns
    -------
    Vc : float
        Predicted critical volume of the chemical, [m^3/mol]
    
    Notes
    -----    
    Using the :obj:`thermo.elements.periodic_table` covalent radii (from RDKit), 
    the coefficient and power should be 4.261206523632586 and 0.5597281770786228
    respectively for best results.
    
    Examples
    --------
    Prediction of critical volume of decane:
        
    >>> Mersmann_Kind_predictor({'C': 10, 'H': 22})
    0.0005851859052024729
    
    This is compared against the experimental value, 0.000624 (a 6.2% relative
    error)
    
    Using custom fitted coefficients we can do a bit better:
        
    >>> from thermo.critical import rcovs_regressed
    >>> Mersmann_Kind_predictor({'C': 10, 'H': 22}, coeff=4.261206523632586, 
    ... power=0.5597281770786228, covalent_radii=rcovs_regressed)
    0.0005956871011923075
    
    The relative error is only 4.5% now. This is compared to an experimental 
    uncertainty of 5.6%.
    
    Evaluating 1321 critical volumes in the database, the average relative
    error is 5.0%; standard deviation 6.8%; and worst value of 79% relative
    error for phosphorus.
    
    References
    ----------
    .. [1] Mersmann, Alfons, and Matthias Kind. "Correlation for the Prediction
       of Critical Molar Volume." Industrial & Engineering Chemistry Research,
       October 16, 2017. https://doi.org/10.1021/acs.iecr.7b03171.
    .. [2] Mersmann, Alfons, and Matthias Kind. "Prediction of Mechanical and 
       Thermal Properties of Pure Liquids, of Critical Data, and of Vapor 
       Pressure." Industrial & Engineering Chemistry Research, January 31, 
       2017. https://doi.org/10.1021/acs.iecr.6b04323.
    '''
    H_RADIUS_COV = covalent_radii['H']
    tot = 0
    atom_count = 0
    for atom, count in atoms.items():
        if atom not in covalent_radii:
            raise Exception('Atom %s is not supported by the supplied dictionary' %atom)
        tot += count*covalent_radii[atom]
        atom_count += count
    da = 2.*tot/atom_count
    ra = da/2.
    da_SI = da*1e-10 # Convert from angstrom to m
    return ((coeff/(ra/H_RADIUS_COV)**power)*da_SI)**3*N_A*atom_count