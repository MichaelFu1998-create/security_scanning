def cliques(graph, threshold=3):
    
    """ Returns all the cliques in the graph of at least the given size.
    """
    
    cliques = []
    for n in graph.nodes:
        c = clique(graph, n.id)
        if len(c) >= threshold: 
            c.sort()
            if c not in cliques:
                cliques.append(c)
    
    return cliques