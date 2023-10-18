def _get_queues(g, queues, edge, edge_type):
    """Used to specify edge indices from different types of arguments."""
    INT = numbers.Integral
    if isinstance(queues, INT):
        queues = [queues]

    elif queues is None:
        if edge is not None:
            if isinstance(edge, tuple):
                if isinstance(edge[0], INT) and isinstance(edge[1], INT):
                    queues = [g.edge_index[edge]]
            elif isinstance(edge[0], collections.Iterable):
                if np.array([len(e) == 2 for e in edge]).all():
                    queues = [g.edge_index[e] for e in edge]
            else:
                queues = [g.edge_index[edge]]
        elif edge_type is not None:
            if isinstance(edge_type, collections.Iterable):
                edge_type = set(edge_type)
            else:
                edge_type = set([edge_type])
            tmp = []
            for e in g.edges():
                if g.ep(e, 'edge_type') in edge_type:
                    tmp.append(g.edge_index[e])

            queues = np.array(tmp, int)

        if queues is None:
            queues = range(g.number_of_edges())

    return queues