def _get_catalysts_in_reaction(reaction: Reaction) -> Set[BaseAbundance]:
    """Return nodes that are both in reactants and reactions in a reaction."""
    return {
        reactant
        for reactant in reaction.reactants
        if reactant in reaction.products
    }