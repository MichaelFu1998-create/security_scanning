def overlay_data(graph: BELGraph,
                 data: Mapping[BaseEntity, Any],
                 label: Optional[str] = None,
                 overwrite: bool = False,
                 ) -> None:
    """Overlays tabular data on the network

    :param graph: A BEL Graph
    :param data: A dictionary of {tuple node: data for that node}
    :param label: The annotation label to put in the node dictionary
    :param overwrite: Should old annotations be overwritten?
    """
    if label is None:
        label = WEIGHT

    for node, value in data.items():
        if node not in graph:
            log.debug('%s not in graph', node)
            continue

        if label in graph.nodes[node] and not overwrite:
            log.debug('%s already on %s', label, node)
            continue

        graph.nodes[node][label] = value