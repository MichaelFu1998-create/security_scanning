def balance_ions(anions, cations, anion_zs=None, cation_zs=None, 
                 anion_concs=None, cation_concs=None, rho_w=997.1, 
                 method='increase dominant', selected_ion=None):
    r'''Performs an ion balance to adjust measured experimental ion 
    compositions to electroneutrality. Can accept either the actual mole 
    fractions of the ions, or their concentrations in units of [mg/L] as well
    for convinience.
    
    The default method will locate the most prevalent ion in the type of 
    ion not in excess - and increase it until the two ion types balance.

    Parameters
    ----------
    anions : list(ChemicalMetadata)
        List of all negatively charged ions measured as being in the solution;
        ChemicalMetadata instances or simply objects with the attributes `MW` 
        and `charge`, [-]
    cations : list(ChemicalMetadata)
        List of all positively charged ions measured as being in the solution;
        ChemicalMetadata instances or simply objects with the attributes `MW` 
        and `charge`, [-]
    anion_zs : list, optional
        Mole fractions of each anion as measured in the aqueous solution, [-]
    cation_zs : list, optional
        Mole fractions of each cation as measured in the aqueous solution, [-]
    anion_concs : list, optional
        Concentrations of each anion in the aqueous solution in the units often
        reported (for convinience only) [mg/L]
    cation_concs : list, optional
        Concentrations of each cation in the aqueous solution in the units 
        often reported (for convinience only) [mg/L]
    rho_w : float, optional
        Density of the aqueous solutionr at the temperature and pressure the
        anion and cation concentrations were measured (if specified), [kg/m^3]
    method : str, optional
        The method to use to balance the ionimbalance; one of 'dominant', 
        'decrease dominant', 'increase dominant',
        'proportional insufficient ions increase', 
        'proportional excess ions decrease', 
        'proportional cation adjustment', 'proportional anion adjustment', 
        'Na or Cl increase', 'Na or Cl decrease', 'adjust', 'increase', 
        'decrease', 'makeup'].
    selected_ion : ChemicalMetadata, optional
        Some methods adjust only one user-specified ion; this is that input.
        For the case of the 'makeup' method, this is a tuple of (anion, cation)
        ChemicalMetadata instances and only the ion type not in excess will be
        used.

    Returns
    -------
    anions : list(ChemicalMetadata)
        List of all negatively charged ions measured as being in the solution;
        ChemicalMetadata instances after potentially adding in an ion which
        was not present but specified by the user, [-]
    cations : list(ChemicalMetadata)
        List of all positively charged ions measured as being in the solution;
        ChemicalMetadata instances after potentially adding in an ion which
        was not present but specified by the user, [-]
    anion_zs : list,
        Mole fractions of each anion in the aqueous solution after the charge
        balance, [-]
    cation_zs : list
        Mole fractions of each cation in the aqueous solution after the charge
        balance, [-]
    z_water : float
        Mole fraction of the water in the solution, [-]

    Notes
    -----
    The methods perform the charge balance as follows:
        
    * 'dominant' : The ion with the largest mole fraction in solution has its
      concentration adjusted up or down as necessary to balance the solution.
    * 'decrease dominant' : The ion with the largest mole fraction in the type
      of ion with *excess* charge has its own mole fraction decreased to balance
      the solution.
    * 'increase dominant' : The ion with the largest mole fraction in the type
      of ion with *insufficient* charge has its own mole fraction decreased to 
      balance the solution.
    * 'proportional insufficient ions increase' : The ion charge type which is
      present insufficiently has each of the ions mole fractions *increased*
      proportionally until the solution is balanced.
    * 'proportional excess ions decrease' :  The ion charge type which is
      present in excess has each of the ions mole fractions *decreased*
      proportionally until the solution is balanced.
    * 'proportional cation adjustment' : All *cations* have their mole fractions
      increased or decreased proportionally as necessary to balance the 
      solution.
    * 'proportional anion adjustment' : All *anions* have their mole fractions
      increased or decreased proportionally as necessary to balance the 
      solution.
    * 'Na or Cl increase' : Either Na+ or Cl- is *added* to the solution until
      the solution is balanced; the species will be added if they were not
      present initially as well.
    * 'Na or Cl decrease' : Either Na+ or Cl- is *removed* from the solution 
      until the solution is balanced; the species will be added if they were 
      not present initially as well.
    * 'adjust' : An ion specified with the parameter `selected_ion` has its
      mole fraction *increased or decreased* as necessary to balance the 
      solution. An exception is raised if the specified ion alone cannot 
      balance the solution.
    * 'increase' : An ion specified with the parameter `selected_ion` has its
      mole fraction *increased* as necessary to balance the 
      solution. An exception is raised if the specified ion alone cannot 
      balance the solution.
    * 'decrease' : An ion specified with the parameter `selected_ion` has its
      mole fraction *decreased* as necessary to balance the 
      solution. An exception is raised if the specified ion alone cannot 
      balance the solution.
    * 'makeup' : Two ions ase specified as a tuple with the parameter 
      `selected_ion`. Whichever ion type is present in the solution 
      insufficiently is added; i.e. if the ions were Mg+2 and Cl-, and there
      was too much negative charge in the solution, Mg+2 would be added until
      the solution was balanced.
        
    Examples
    --------
    >>> anions_n = ['Cl-', 'HCO3-', 'SO4-2']
    >>> cations_n = ['Na+', 'K+', 'Ca+2', 'Mg+2']
    >>> cations = [pubchem_db.search_name(i) for i in cations_n]
    >>> anions = [pubchem_db.search_name(i) for i in anions_n]
    >>> an_res, cat_res, an_zs, cat_zs, z_water = balance_ions(anions, cations,
    ... anion_zs=[0.02557, 0.00039, 0.00026], cation_zs=[0.0233, 0.00075,
    ... 0.00262, 0.00119], method='proportional excess ions decrease')
    >>> an_zs
    [0.02557, 0.00039, 0.00026]
    >>> cat_zs
    [0.01948165456267761, 0.0006270918850647299, 0.0021906409851594564, 0.0009949857909693717]
    >>> z_water
    0.9504856267761288
    
    References
    ----------
    '''
    anions = list(anions)
    cations = list(cations)
    n_anions = len(anions)
    n_cations = len(cations)
    ions = anions + cations
    anion_charges = [i.charge for i in anions]
    cation_charges = [i.charge for i in cations]
    charges = anion_charges + cation_charges + [0]

    MW_water = [18.01528]
    rho_w = rho_w/1000 # Convert to kg/liter
    
    if anion_concs is not None and cation_concs is not None:
        anion_ws = [i*1E-6/rho_w for i in anion_concs]
        cation_ws = [i*1E-6/rho_w for i in cation_concs]
        w_water = 1 - sum(anion_ws) - sum(cation_ws)
    
        anion_MWs = [i.MW for i in anions]
        cation_MWs = [i.MW for i in cations]
        MWs = anion_MWs + cation_MWs + MW_water
        zs = ws_to_zs(anion_ws + cation_ws + [w_water], MWs)
    else:
        if anion_zs is None or cation_zs is None:
            raise Exception('Either both of anion_concs and cation_concs or '
                            'anion_zs and cation_zs must be specified.')
        else:
            zs = anion_zs + cation_zs
            zs = zs + [1 - sum(zs)]
    
    impacts = [zi*ci for zi, ci in zip(zs, charges)]
    balance_error = sum(impacts)
    
    
    if abs(balance_error) < 1E-7:
        anion_zs = zs[0:n_anions]
        cation_zs = zs[n_anions:n_cations+n_anions]
        z_water = zs[-1]
        return anions, cations, anion_zs, cation_zs, z_water
    if 'dominant' in method:
        anion_zs, cation_zs, z_water = ion_balance_dominant(impacts,
            balance_error, charges, zs, n_anions, n_cations, method)
        return anions, cations, anion_zs, cation_zs, z_water
    elif 'proportional' in method:
        anion_zs, cation_zs, z_water = ion_balance_proportional(
            anion_charges, cation_charges, zs, n_anions, n_cations,
            balance_error, method)
        return anions, cations, anion_zs, cation_zs, z_water
    elif method == 'Na or Cl increase':
        increase = True
        if balance_error < 0:
            selected_ion = pubchem_db.search_name('Na+')
        else:
            selected_ion = pubchem_db.search_name('Cl-')
    elif method == 'Na or Cl decrease':
        increase = False
        if balance_error > 0:
            selected_ion = pubchem_db.search_name('Na+')
        else:
            selected_ion = pubchem_db.search_name('Cl-')
    # All of the below work with the variable selected_ion
    elif method == 'adjust':
        # A single ion will be increase or decreased to fix the balance automatically
        increase = None
    elif method == 'increase':
        increase = True
        # Raise exception if approach doesn't work
    elif method == 'decrease':
        increase = False
        # Raise exception if approach doesn't work
    elif method == 'makeup':
        # selected ion starts out as a tuple in this case; always adding the compound
        increase = True
        if balance_error < 0:
            selected_ion = selected_ion[1]
        else:
            selected_ion = selected_ion[0]
    else:
        raise Exception('Method not recognized')
    if selected_ion is None:
        raise Exception("For methods 'adjust', 'increase', 'decrease', and "
                        "'makeup', an ion must be specified with the "
                        "`selected_ion` parameter")
        
    anion_zs, cation_zs, z_water = ion_balance_adjust_wrapper(charges, zs, n_anions, n_cations,
                                                              anions, cations, selected_ion, increase=increase)
    return anions, cations, anion_zs, cation_zs, z_water