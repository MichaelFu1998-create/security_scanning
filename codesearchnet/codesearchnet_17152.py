def get_names_including_errors_by_namespace(graph: BELGraph, namespace: str) -> Set[str]:
    """Takes the names from the graph in a given namespace (:func:`pybel.struct.summary.get_names_by_namespace`) and
    the erroneous names from the same namespace (:func:`get_incorrect_names_by_namespace`) and returns them together
    as a unioned set

    :return: The set of all correct and incorrect names from the given namespace in the graph
    """
    return get_names_by_namespace(graph, namespace) | get_incorrect_names_by_namespace(graph, namespace)