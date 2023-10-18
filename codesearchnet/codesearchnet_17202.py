def build_spia_matrices(nodes: Set[str]) -> Dict[str, pd.DataFrame]:
    """Build an adjacency matrix for each KEGG relationship and return in a dictionary.

    :param nodes: A set of HGNC gene symbols
    :return: Dictionary of adjacency matrix for each relationship
    """
    nodes = list(sorted(nodes))

    # Create sheets of the excel in the given order
    matrices = OrderedDict()
    for relation in KEGG_RELATIONS:
        matrices[relation] = pd.DataFrame(0, index=nodes, columns=nodes)

    return matrices