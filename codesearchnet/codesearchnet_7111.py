def simple_formula_parser(formula):
    r'''Basic formula parser, primarily for obtaining element counts from 
    formulas as formated in PubChem. Handles formulas with integer counts, 
    but no brackets, no hydrates, no charges, no isotopes, and no group
    multipliers.
    
    Strips charges from the end of a formula first. Accepts repeated chemical
    units. Performs no sanity checking that elements are actually elements.
    As it uses regular expressions for matching, errors are mostly just ignored.
    
    Parameters
    ----------
    formula : str
        Formula string, very simply formats only.

    Returns
    -------
    atoms : dict
        dictionary of counts of individual atoms, indexed by symbol with
        proper capitalization, [-]

    Notes
    -----
    Inspiration taken from the thermopyl project, at
    https://github.com/choderalab/thermopyl.

    Examples
    --------
    >>> simple_formula_parser('CO2')
    {'C': 1, 'O': 2}
    '''
    formula = formula.split('+')[0].split('-')[0]
    groups = _formula_p1.split(formula)[1::2]
    cnt = Counter()
    for group in groups:
        ele, count = _formula_p2.split(group)[1:]
        cnt[ele] += int(count) if count.isdigit() else 1
    return dict(cnt)