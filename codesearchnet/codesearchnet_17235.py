def complex_has_member(graph: BELGraph, complex_node: ComplexAbundance, member_node: BaseEntity) -> bool:
    """Does the given complex contain the member?"""
    return any(  # TODO can't you look in the members of the complex object (if it's enumerated)
        v == member_node
        for _, v, data in graph.out_edges(complex_node, data=True)
        if data[RELATION] == HAS_COMPONENT
    )