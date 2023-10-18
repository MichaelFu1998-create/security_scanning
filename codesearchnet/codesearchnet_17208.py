def overlay_type_data(graph: BELGraph,
                      data: Mapping[str, float],
                      func: str,
                      namespace: str,
                      label: Optional[str] = None,
                      overwrite: bool = False,
                      impute: Optional[float] = None,
                      ) -> None:
    """Overlay tabular data on the network for data that comes from an data set with identifiers that lack
    namespaces.

    For example, if you want to overlay differential gene expression data from a table, that table
    probably has HGNC identifiers, but no specific annotations that they are in the HGNC namespace or
    that the entities to which they refer are RNA.

    :param graph: A BEL Graph
    :param dict data: A dictionary of {name: data}
    :param func: The function of the keys in the data dictionary
    :param namespace: The namespace of the keys in the data dictionary
    :param label: The annotation label to put in the node dictionary
    :param overwrite: Should old annotations be overwritten?
    :param impute: The value to use for missing data
    """
    new_data = {
        node: data.get(node[NAME], impute)
        for node in filter_nodes(graph, function_namespace_inclusion_builder(func, namespace))
    }

    overlay_data(graph, new_data, label=label, overwrite=overwrite)