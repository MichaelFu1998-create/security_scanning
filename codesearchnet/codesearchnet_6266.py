def ast2str(expr, level=0, names=None):
    """convert compiled ast to gene_reaction_rule str

    Parameters
    ----------
    expr : str
        string for a gene reaction rule, e.g "a and b"
    level : int
        internal use only
    names : dict
        Dict where each element id a gene identifier and the value is the
        gene name. Use this to get a rule str which uses names instead. This
        should be done for display purposes only. All gene_reaction_rule
        strings which are computed with should use the id.

    Returns
    ------
    string
        The gene reaction rule
    """
    if isinstance(expr, Expression):
        return ast2str(expr.body, 0, names) \
            if hasattr(expr, "body") else ""
    elif isinstance(expr, Name):
        return names.get(expr.id, expr.id) if names else expr.id
    elif isinstance(expr, BoolOp):
        op = expr.op
        if isinstance(op, Or):
            str_exp = " or ".join(ast2str(i, level + 1, names)
                                  for i in expr.values)
        elif isinstance(op, And):
            str_exp = " and ".join(ast2str(i, level + 1, names)
                                   for i in expr.values)
        else:
            raise TypeError("unsupported operation " + op.__class__.__name)
        return "(" + str_exp + ")" if level else str_exp
    elif expr is None:
        return ""
    else:
        raise TypeError("unsupported operation  " + repr(expr))