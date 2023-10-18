def ion_balance_proportional(anion_charges, cation_charges, zs, n_anions, 
                             n_cations, balance_error, method):
    '''Helper method for balance_ions for the proportional family of methods. 
    See balance_ions for a description of the methods; parameters are fairly
    obvious.
    '''
    anion_zs = zs[0:n_anions]
    cation_zs = zs[n_anions:n_cations+n_anions]
    anion_balance_error = sum([zi*ci for zi, ci in zip(anion_zs, anion_charges)])
    cation_balance_error = sum([zi*ci for zi, ci in zip(cation_zs, cation_charges)])
    if method == 'proportional insufficient ions increase':
        if balance_error < 0:
            multiplier = -anion_balance_error/cation_balance_error
            cation_zs = [i*multiplier for i in cation_zs]
        else:
            multiplier = -cation_balance_error/anion_balance_error
            anion_zs = [i*multiplier for i in anion_zs]
    elif method == 'proportional excess ions decrease':
        if balance_error < 0:
            multiplier = -cation_balance_error/anion_balance_error
            anion_zs = [i*multiplier for i in anion_zs]
        else:
            multiplier = -anion_balance_error/cation_balance_error
            cation_zs = [i*multiplier for i in cation_zs]
    elif method == 'proportional cation adjustment':
        multiplier = -anion_balance_error/cation_balance_error
        cation_zs = [i*multiplier for i in cation_zs]
    elif method == 'proportional anion adjustment':
        multiplier = -cation_balance_error/anion_balance_error
        anion_zs = [i*multiplier for i in anion_zs]
    else:
        raise Exception('Allowable methods are %s' %charge_balance_methods)
    z_water = 1. - sum(anion_zs) - sum(cation_zs)
    return anion_zs, cation_zs, z_water