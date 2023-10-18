def eigenvector_centrality(graph, normalized=True, reversed=True, rating={},
                           start=None, iterations=100, tolerance=0.0001):

    """ Eigenvector centrality for nodes in the graph (like Google's PageRank).
    
    Eigenvector centrality is a measure of the importance of a node in a directed network. 
    It rewards nodes with a high potential of (indirectly) connecting to high-scoring nodes.
    Nodes with no incoming connections have a score of zero.
    If you want to measure outgoing connections, reversed should be False.

    The eigenvector calculation is done by the power iteration method.
    It has no guarantee of convergence.
    A starting vector for the power iteration can be given in the start dict.
    
    You can adjust the importance of a node with the rating dictionary,
    which links node id's to a score.
    
    The algorithm is adapted from NetworkX, Aric Hagberg (hagberg@lanl.gov):
    https://networkx.lanl.gov/attachment/ticket/119/eigenvector_centrality.py

    """

    G = graph.keys()     
    W = adjacency (graph, directed=True, reversed=reversed)

    def _normalize(x):
        s = sum(x.values())
        if s != 0: s = 1.0 / s
        for k in x: 
            x[k] *= s
    
    x = start
    if x is None:
        x = dict([(n, random()) for n in G])
    _normalize(x)

    # Power method: y = Ax multiplication.
    for i in range(iterations):
        x0 = x
        x = dict.fromkeys(x0.keys(), 0)
        for n in x:
            for nbr in W[n]:
                r = 1
                if rating.has_key(n): r = rating[n]
                x[n] += 0.01 + x0[nbr] * W[n][nbr] * r
        _normalize(x)          
        e = sum([abs(x[n]-x0[n]) for n in x])
        if e < len(graph.nodes) * tolerance:
            if normalized:
                # Normalize between 0.0 and 1.0.
                m = max(x.values())
                if m == 0: m = 1
                x = dict([(id, w/m) for id, w in x.iteritems()])
            return x

    #raise NoConvergenceError
    warn("node weight is 0 because eigenvector_centrality() did not converge.", Warning)
    return dict([(n, 0) for n in G])