def _adjacency_adjust(adjacency, adjust, is_directed):
    """Takes an adjacency list and returns a (possibly) modified
    adjacency list.
    """

    for v, adj in adjacency.items():
        for properties in adj.values():
            if properties.get('edge_type') is None:
                properties['edge_type'] = 1

    if is_directed:
        if adjust == 2:
            null_nodes = set()

            for k, adj in adjacency.items():
                if len(adj) == 0:
                    null_nodes.add(k)

            for k, adj in adjacency.items():
                for v in adj.keys():
                    if v in null_nodes:
                        adj[v]['edge_type'] = 0

        else:
            for k, adj in adjacency.items():
                if len(adj) == 0:
                    adj[k] = {'edge_type': 0}

    return adjacency