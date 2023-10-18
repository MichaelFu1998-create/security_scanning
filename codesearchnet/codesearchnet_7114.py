def serialize_formula(formula):
    r'''Basic formula serializer to construct a consistently-formatted formula.
    This is necessary for handling user-supplied formulas, which are not always
    well formatted.

    Performs no sanity checking that elements are actually elements.
    
    Parameters
    ----------
    formula : str
        Formula string as parseable by the method nested_formula_parser, [-]

    Returns
    -------
    formula : str
        A consistently formatted formula to describe a molecular formula, [-]

    Notes
    -----

    Examples
    --------
    >>> serialize_formula('Pd(NH3)4+3')
    'H12N4Pd+3'
    '''
    charge = charge_from_formula(formula)
    element_dict = nested_formula_parser(formula)
    base = atoms_to_Hill(element_dict)
    if charge  == 0:
        pass
    elif charge > 0:
        if charge == 1:
            base += '+'
        else:
            base += '+' + str(charge)
    elif charge < 0:
        if charge == -1:
            base += '-'
        else:
            base +=  str(charge)
    return base