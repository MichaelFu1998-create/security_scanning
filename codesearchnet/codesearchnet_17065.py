def list_abundance_cartesian_expansion(graph: BELGraph) -> None:
    """Expand all list abundances to simple subject-predicate-object networks."""
    for u, v, k, d in list(graph.edges(keys=True, data=True)):
        if CITATION not in d:
            continue

        if isinstance(u, ListAbundance) and isinstance(v, ListAbundance):
            for u_member, v_member in itt.product(u.members, v.members):
                graph.add_qualified_edge(
                    u_member, v_member,
                    relation=d[RELATION],
                    citation=d.get(CITATION),
                    evidence=d.get(EVIDENCE),
                    annotations=d.get(ANNOTATIONS),
                )

        elif isinstance(u, ListAbundance):
            for member in u.members:
                graph.add_qualified_edge(
                    member, v,
                    relation=d[RELATION],
                    citation=d.get(CITATION),
                    evidence=d.get(EVIDENCE),
                    annotations=d.get(ANNOTATIONS),
                )

        elif isinstance(v, ListAbundance):
            for member in v.members:
                graph.add_qualified_edge(
                    u, member,
                    relation=d[RELATION],
                    citation=d.get(CITATION),
                    evidence=d.get(EVIDENCE),
                    annotations=d.get(ANNOTATIONS),
                )

    _remove_list_abundance_nodes(graph)