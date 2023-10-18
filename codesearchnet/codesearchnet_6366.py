def reaction_elements(reaction):
    """
    Split metabolites into the atoms times their stoichiometric coefficients.

    Parameters
    ----------
    reaction : Reaction
        The metabolic reaction whose components are desired.

    Returns
    -------
    list
        Each of the reaction's metabolites' desired carbon elements (if any)
        times that metabolite's stoichiometric coefficient.
    """
    c_elements = [coeff * met.elements.get('C', 0)
                  for met, coeff in iteritems(reaction.metabolites)]
    return [elem for elem in c_elements if elem != 0]