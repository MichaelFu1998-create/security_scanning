def reaction_weight(reaction):
    """Return the metabolite weight times its stoichiometric coefficient."""

    if len(reaction.metabolites) != 1:
        raise ValueError('Reaction weight is only defined for single '
                         'metabolite products or educts.')

    met, coeff = next(iteritems(reaction.metabolites))

    return [coeff * met.formula_weight]