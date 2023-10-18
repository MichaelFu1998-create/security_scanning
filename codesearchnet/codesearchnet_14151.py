def partition(graph):
    
    """ Splits unconnected subgraphs.
    
    For each node in the graph, make a list of its id and all directly connected id's.
    If one of the nodes in this list intersects with a subgraph,
    they are all part of that subgraph.
    Otherwise, this list is part of a new subgraph.
    Return a list of subgraphs sorted by size (biggest-first).
    
    """
    
    g = []
    for n in graph.nodes:
        c = [n.id for n in flatten(n)]
        f = False
        for i in range(len(g)):
            if len(intersection(g[i], c)) > 0:
                g[i] = union(g[i], c)
                f = True
                break
        if not f:
            g.append(c)
    
    # If 1 is directly connected to 2 and 3,
    # and 4 is directly connected to 5 and 6, these are separate subgraphs.
    # If we later find that 7 is directly connected to 3 and 6,
    # it will be attached to [1, 2, 3] yielding
    # [1, 2, 3, 6, 7] and [4, 5, 6].
    # These two subgraphs are connected and need to be merged.
    merged = []
    for i in range(len(g)):
        merged.append(g[i])
        for j in range(i+1, len(g)):
            if len(intersection(g[i], g[j])) > 0:
                merged[-1].extend(g[j])
                g[j] = []
    
    g = merged
    g = [graph.sub(g, distance=0) for g in g]
    g.sort(lambda a, b: len(b) - len(a))             
    
    return g