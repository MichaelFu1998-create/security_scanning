def flatten_list_abundance(node: ListAbundance) -> ListAbundance:
    """Flattens the complex or composite abundance."""
    return node.__class__(list(chain.from_iterable(
        (
            flatten_list_abundance(member).members
            if isinstance(member, ListAbundance) else
            [member]
        )
        for member in node.members
    )))