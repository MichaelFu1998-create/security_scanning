def analyze_number(var, err=''):
    """ Analyse number for type and split from unit
        1px -> (q, 'px')
    args:
        var (str): number string
    kwargs:
        err (str): Error message
    raises:
        SyntaxError
    returns:
        tuple
    """
    n, u = split_unit(var)
    if not isinstance(var, string_types):
        return (var, u)
    if is_color(var):
        return (var, 'color')
    if is_int(n):
        n = int(n)
    elif is_float(n):
        n = float(n)
    else:
        raise SyntaxError('%s ´%s´' % (err, var))
    return (n, u)