def summarize_stability(graph: BELGraph) -> Mapping[str, int]:
    """Summarize the stability of the graph."""
    regulatory_pairs = get_regulatory_pairs(graph)
    chaotic_pairs = get_chaotic_pairs(graph)
    dampened_pairs = get_dampened_pairs(graph)
    contraditory_pairs = get_contradiction_summary(graph)
    separately_unstable_triples = get_separate_unstable_correlation_triples(graph)
    mutually_unstable_triples = get_mutually_unstable_correlation_triples(graph)
    jens_unstable_triples = get_jens_unstable(graph)
    increase_mismatch_triples = get_increase_mismatch_triplets(graph)
    decrease_mismatch_triples = get_decrease_mismatch_triplets(graph)
    chaotic_triples = get_chaotic_triplets(graph)
    dampened_triples = get_dampened_triplets(graph)

    return {
        'Regulatory Pairs': _count_or_len(regulatory_pairs),
        'Chaotic Pairs': _count_or_len(chaotic_pairs),
        'Dampened Pairs': _count_or_len(dampened_pairs),
        'Contradictory Pairs': _count_or_len(contraditory_pairs),
        'Separately Unstable Triples': _count_or_len(separately_unstable_triples),
        'Mutually Unstable Triples': _count_or_len(mutually_unstable_triples),
        'Jens Unstable Triples': _count_or_len(jens_unstable_triples),
        'Increase Mismatch Triples': _count_or_len(increase_mismatch_triples),
        'Decrease Mismatch Triples': _count_or_len(decrease_mismatch_triples),
        'Chaotic Triples': _count_or_len(chaotic_triples),
        'Dampened Triples': _count_or_len(dampened_triples)
    }