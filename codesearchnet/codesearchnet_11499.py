def iter_complete_graphs(start, stop, factory=None):
    """Iterate over complete graphs.

    Args:
        start (int/iterable):
            Define the size of the starting graph.
            If an int, the nodes will be index-labeled, otherwise should be an iterable of node
            labels.

        stop (int):
            Stops yielding graphs when the size equals stop.

        factory (iterator, optional):
            If provided, nodes added will be labeled according to the values returned by factory.
            Otherwise the extra nodes will be index-labeled.

    Yields:
        :class:`nx.Graph`

    """
    _, nodes = start
    nodes = list(nodes)  # we'll be appending

    if factory is None:
        factory = count()

    while len(nodes) < stop:
        # we need to construct a new graph each time, this is actually faster than copy and add
        # the new edges in any case
        G = nx.complete_graph(nodes)
        yield G

        v = next(factory)
        while v in G:
            v = next(factory)

        nodes.append(v)