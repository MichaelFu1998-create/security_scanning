def calculate_concordance_by_annotation(graph, annotation, key, cutoff=None):
    """Returns the concordance scores for each stratified graph based on the given annotation

    :param pybel.BELGraph graph: A BEL graph
    :param str annotation: The annotation to group by.
    :param str key: The node data dictionary key storing the logFC
    :param float cutoff: The optional logFC cutoff for significance
    :rtype: dict[str,tuple]
    """
    return {
        value: calculate_concordance(subgraph, key, cutoff=cutoff)
        for value, subgraph in get_subgraphs_by_annotation(graph, annotation).items()
    }