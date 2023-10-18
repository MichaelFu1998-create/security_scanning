def charge_from_formula(formula):
    r'''Basic formula parser to determine the charge from a formula - given
    that the charge is already specified as one element of the formula.

    Performs no sanity checking that elements are actually elements.
    
    Parameters
    ----------
    formula : str
        Formula string, very simply formats only, ending in one of '+x',
        '-x', n*'+', or n*'-' or any of them surrounded by brackets but always
        at the end of a formula.

    Returns
    -------
    charge : int
        Charge of the molecule, [faraday]

    Notes
    -----

    Examples
    --------
    >>> charge_from_formula('Br3-')
    -1
    >>> charge_from_formula('Br3(-)')
    -1
    '''
    negative = '-' in formula
    positive = '+' in formula
    if positive and negative:
        raise ValueError('Both negative and positive signs were found in the formula; only one sign is allowed')
    elif not (positive or negative):
        return 0
    multiplier, sign = (-1, '-') if negative else (1, '+')
    
    hit = False
    if '(' in formula:
        hit = bracketed_charge_re.findall(formula)
        if hit:
            formula = hit[-1].replace('(', '').replace(')', '')

    count = formula.count(sign)
    if count == 1:
        splits = formula.split(sign)
        if splits[1] == '' or splits[1] == ')':
            return multiplier
        else:
            return multiplier*int(splits[1])
    else:
        return multiplier*count