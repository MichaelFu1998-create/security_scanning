def read_list_edges(filename, directed=True, **kwargs):
    """Read a file (containing list of edges) and convert it into a directed
    or undirected networkx graph.

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
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    for idx, row in data.iterrows():
        try:
            score = row["Score"]
        except KeyError:
            score = 1
        graph.add_edge(row['Cause'], row["Effect"], weight=score)

    return graph