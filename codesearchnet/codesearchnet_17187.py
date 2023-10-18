def get_network_summary_dict(graph: BELGraph) -> Mapping:
    """Create a summary dictionary."""
    return dict(
        # Counters
        function_count=count_functions(graph),
        modifications_count=get_modifications_count(graph),
        relation_count=count_relations(graph),
        authors_count=count_authors(graph).most_common(15),
        variants_count=count_variants(graph),
        namespaces_count=count_namespaces(graph),
        hub_data={
            (
                node.name or node.identifier
                if NAME in node or IDENTIFIER in node else
                str(node)
            ): degree
            for node, degree in get_top_hubs(graph, n=15)
        },
        disease_data={
            (
                node.name or node.identifier
                if NAME in node or IDENTIFIER in node else
                str(node)
            ): count
            for node, count in get_top_pathologies(graph, n=15)
        },
        # BioGrammar
        regulatory_pairs=[
            get_pair_tuple(u, v)
            for u, v in get_regulatory_pairs(graph)
        ],
        unstable_pairs=list(itt.chain(
            (get_pair_tuple(u, v) + ('Chaotic',) for u, v, in get_chaotic_pairs(graph)),
            (get_pair_tuple(u, v) + ('Dampened',) for u, v, in get_dampened_pairs(graph)),
        )),
        contradictory_pairs=[
            get_pair_tuple(u, v) + (relation,)
            for u, v, relation in get_contradiction_summary(graph)
        ],
        contradictory_triplets=list(itt.chain(
            (get_triplet_tuple(a, b, c) + ('Separate',) for a, b, c in
             get_separate_unstable_correlation_triples(graph)),
            (get_triplet_tuple(a, b, c) + ('Mutual',) for a, b, c in get_mutually_unstable_correlation_triples(graph)),
            (get_triplet_tuple(a, b, c) + ('Jens',) for a, b, c in get_jens_unstable(graph)),
            (get_triplet_tuple(a, b, c) + ('Increase Mismatch',) for a, b, c in get_increase_mismatch_triplets(graph)),
            (get_triplet_tuple(a, b, c) + ('Decrease Mismatch',) for a, b, c in get_decrease_mismatch_triplets(graph)),
        )),
        unstable_triplets=list(itt.chain(
            (get_triplet_tuple(a, b, c) + ('Chaotic',) for a, b, c in get_chaotic_triplets(graph)),
            (get_triplet_tuple(a, b, c) + ('Dampened',) for a, b, c in get_dampened_triplets(graph)),
        )),
        causal_pathologies=sorted({
            get_pair_tuple(u, v) + (graph[u][v][k][RELATION],)
            for u, v, k in filter_edges(graph, has_pathology_causal)
        }),
        # Misc.
        undefined_namespaces=get_undefined_namespaces(graph),
        undefined_annotations=get_undefined_annotations(graph),
        namespaces_with_incorrect_names=get_namespaces_with_incorrect_names(graph),
        unused_namespaces=get_unused_namespaces(graph),
        unused_annotations=get_unused_annotations(graph),
        unused_list_annotation_values=get_unused_list_annotation_values(graph),
        naked_names=get_naked_names(graph),
        error_count=count_error_types(graph),
        # Errors
        error_groups=get_most_common_errors(graph),
        syntax_errors=get_syntax_errors(graph),
        # Bibliometrics
        citation_years=get_citation_years(graph),
        confidence_count=count_confidences(graph),
    )