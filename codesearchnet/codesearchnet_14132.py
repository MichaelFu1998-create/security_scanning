def adjacency(graph, directed=False, reversed=False, stochastic=False, heuristic=None):
    
    """ An edge weight map indexed by node id's.
    
    A dictionary indexed by node id1's in which each value is a
    dictionary of connected node id2's linking to the edge weight.
    If directed, edges go from id1 to id2, but not the other way.
    If stochastic, all the weights for the neighbors of a given node sum to 1.
    A heuristic can be a function that takes two node id's and returns
    and additional cost for movement between the two nodes.
    
    """
    
    v = {}
    for n in graph.nodes:
        v[n.id] = {}
    
    for e in graph.edges:
        
        id1 = e.node1.id
        id2 = e.node2.id
        if reversed:
            id1, id2 = id2, id1
            
        #if not v.has_key(id1): v[id1] = {}
        #if not v.has_key(id2): v[id2] = {}
        v[id1][id2] = 1.0 - e.weight*0.5
        
        if heuristic:
            v[id1][id2] += heuristic(id1, id2)
        
        if not directed: 
            v[id2][id1] = v[id1][id2]
        
    if stochastic:
        for id1 in v:
            d = sum(v[id1].values())
            for id2 in v[id1]: 
                v[id1][id2] /= d
    
    return v