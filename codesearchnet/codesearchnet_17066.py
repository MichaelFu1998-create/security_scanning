def _reaction_cartesion_expansion_unqualified_helper(
        graph: BELGraph,
        u: BaseEntity,
        v: BaseEntity,
        d: dict,
) -> None:
    """Helper to deal with cartension expansion in unqualified edges."""
    if isinstance(u, Reaction) and isinstance(v, Reaction):
        enzymes = _get_catalysts_in_reaction(u) | _get_catalysts_in_reaction(v)

        for reactant, product in chain(itt.product(u.reactants, u.products),
                                       itt.product(v.reactants, v.products)):
            if reactant in enzymes or product in enzymes:
                continue

            graph.add_unqualified_edge(
                reactant, product, INCREASES
            )
        for product, reactant in itt.product(u.products, u.reactants):

            if reactant in enzymes or product in enzymes:
                continue

            graph.add_unqualified_edge(
                product, reactant, d[RELATION],
            )

    elif isinstance(u, Reaction):

        enzymes = _get_catalysts_in_reaction(u)

        for product in u.products:

            # Skip create increases edges between enzymes
            if product in enzymes:
                continue

            # Only add edge between v and reaction if the node is not part of the reaction
            # In practice skips hasReactant, hasProduct edges
            if v not in u.products and v not in u.reactants:
                graph.add_unqualified_edge(
                    product, v, INCREASES
                )
            for reactant in u.reactants:
                graph.add_unqualified_edge(
                    reactant, product, INCREASES
                )

    elif isinstance(v, Reaction):

        enzymes = _get_catalysts_in_reaction(v)

        for reactant in v.reactants:

            # Skip create increases edges between enzymes
            if reactant in enzymes:
                continue

            # Only add edge between v and reaction if the node is not part of the reaction
            # In practice skips hasReactant, hasProduct edges
            if u not in v.products and u not in v.reactants:
                graph.add_unqualified_edge(
                    u, reactant, INCREASES
                )
            for product in v.products:
                graph.add_unqualified_edge(
                    reactant, product, INCREASES
                )