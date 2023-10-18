def generate_bioprocess_mechanisms(graph, key: Optional[str] = None) -> Mapping[BiologicalProcess, BELGraph]:
    """Generate a mechanistic sub-graph for each biological process in the graph using :func:`generate_mechanism`.

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data.
    """
    return {
        biological_process: generate_mechanism(graph, biological_process, key=key)
        for biological_process in get_nodes_by_function(graph, BIOPROCESS)
    }