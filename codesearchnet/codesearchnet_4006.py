def read_adjacency_matrix(filename, directed=True, **kwargs):
    """Read a file (containing an adjacency matrix) and convert it into a
    directed or undirected networkx graph.

    :param filename: file to read or DataFrame containing the data
    :type filename: str or pandas.DataFrame
    :param directed: Return directed graph
    :type directed: bool
    :param kwargs: extra parameters to be passed to pandas.read_csv
    :return: networkx graph containing the graph.
    :rtype: **networkx.DiGraph** or **networkx.Graph** depending on the
      ``directed`` parameter.
    """
    if isinstance(filename, str):
        data = read_csv(filename, **kwargs)
    elif isinstance(filename, DataFrame):
        data = filename
    else:
        raise TypeError("Type not supported.")
    if directed:
        return nx.relabel_nodes(nx.DiGraph(data.values),
                                {idx: i for idx, i in enumerate(data.columns)})
    else:
        return nx.relabel_nodes(nx.Graph(data.values),
                                {idx: i for idx, i in enumerate(data.columns)})