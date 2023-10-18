def eval_gpr(expr, knockouts):
    """evaluate compiled ast of gene_reaction_rule with knockouts

    Parameters
    ----------
    expr : Expression
        The ast of the gene reaction rule
    knockouts : DictList, set
        Set of genes that are knocked out

    Returns
    -------
    bool
        True if the gene reaction rule is true with the given knockouts
        otherwise false
    """
    if isinstance(expr, Expression):
        return eval_gpr(expr.body, knockouts)
    elif isinstance(expr, Name):
        return expr.id not in knockouts
    elif isinstance(expr, BoolOp):
        op = expr.op
        if isinstance(op, Or):
            return any(eval_gpr(i, knockouts) for i in expr.values)
        elif isinstance(op, And):
            return all(eval_gpr(i, knockouts) for i in expr.values)
        else:
            raise TypeError("unsupported operation " + op.__class__.__name__)
    elif expr is None:
        return True
    else:
        raise TypeError("unsupported operation  " + repr(expr))