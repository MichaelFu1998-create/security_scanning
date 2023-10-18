def reaction_cartesian_expansion(graph: BELGraph, accept_unqualified_edges: bool = True) -> None:
    """Expand all reactions to simple subject-predicate-object networks."""
    for u, v, d in list(graph.edges(data=True)):
        # Deal with unqualified edges
        if CITATION not in d and accept_unqualified_edges:
            _reaction_cartesion_expansion_unqualified_helper(graph, u, v, d)
            continue

        if isinstance(u, Reaction) and isinstance(v, Reaction):
            catalysts = _get_catalysts_in_reaction(u) | _get_catalysts_in_reaction(v)

            for reactant, product in chain(itt.product(u.reactants, u.products), itt.product(v.reactants, v.products)):
                if reactant in catalysts or product in catalysts:
                    continue
                graph.add_increases(
                    reactant, product,
                    citation=d.get(CITATION),
                    evidence=d.get(EVIDENCE),
                    annotations=d.get(ANNOTATIONS),
                )

            for product, reactant in itt.product(u.products, u.reactants):
                if reactant in catalysts or product in catalysts:
                    continue

                graph.add_qualified_edge(
                    product, reactant,
                    relation=d[RELATION],
                    citation=d.get(CITATION),
                    evidence=d.get(EVIDENCE),
                    annotations=d.get(ANNOTATIONS),
                )

        elif isinstance(u, Reaction):
            catalysts = _get_catalysts_in_reaction(u)

            for product in u.products:
                # Skip create increases edges between enzymes
                if product in catalysts:
                    continue

                # Only add edge between v and reaction if the node is not part of the reaction
                # In practice skips hasReactant, hasProduct edges
                if v not in u.products and v not in u.reactants:
                    graph.add_increases(
                        product, v,
                        citation=d.get(CITATION),
                        evidence=d.get(EVIDENCE),
                        annotations=d.get(ANNOTATIONS),
                    )

                for reactant in u.reactants:
                    graph.add_increases(
                        reactant, product,
                        citation=d.get(CITATION),
                        evidence=d.get(EVIDENCE),
                        annotations=d.get(ANNOTATIONS),
                    )

        elif isinstance(v, Reaction):
            for reactant in v.reactants:
                catalysts = _get_catalysts_in_reaction(v)

                # Skip create increases edges between enzymes
                if reactant in catalysts:
                    continue

                # Only add edge between v and reaction if the node is not part of the reaction
                # In practice skips hasReactant, hasProduct edges
                if u not in v.products and u not in v.reactants:
                    graph.add_increases(
                        u, reactant,
                        citation=d.get(CITATION),
                        evidence=d.get(EVIDENCE),
                        annotations=d.get(ANNOTATIONS),
                    )
                for product in v.products:
                    graph.add_increases(
                        reactant, product,
                        citation=d.get(CITATION),
                        evidence=d.get(EVIDENCE),
                        annotations=d.get(ANNOTATIONS),
                    )

    _remove_reaction_nodes(graph)