def get_modifications_count(graph: BELGraph) -> Mapping[str, int]:
    """Get a modifications count dictionary."""
    return remove_falsy_values({
        'Translocations': len(get_translocated(graph)),
        'Degradations': len(get_degradations(graph)),
        'Molecular Activities': len(get_activities(graph)),
    })