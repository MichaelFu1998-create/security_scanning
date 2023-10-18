def make_factor(var, e, bn):
    """Return the factor for var in bn's joint distribution given e.
    That is, bn's full joint distribution, projected to accord with e,
    is the pointwise product of these factors for bn's variables."""
    node = bn.variable_node(var)
    vars = [X for X in [var] + node.parents if X not in e]
    cpt = dict((event_values(e1, vars), node.p(e1[var], e1))
               for e1 in all_events(vars, bn, e))
    return Factor(vars, cpt)