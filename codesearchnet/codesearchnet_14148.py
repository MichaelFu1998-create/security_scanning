def subgraph(graph, id, distance=1):
    
    """ Creates the subgraph of the flattened node with given id (or list of id's).
    Finds all the edges between the nodes that make up the subgraph.
    """
    
    g = graph.copy(empty=True)
    
    if isinstance(id, (FunctionType, LambdaType)):
        # id can also be a lambda or function that returns True or False
        # for each node in the graph. We take the id's of nodes that pass.
        id = [node.id for node in filter(id, graph.nodes)]
    if not isinstance(id, (list, tuple)):
        id = [id]
    for id in id:
        for n in flatten(graph[id], distance):
            g.add_node(n.id, n.r, n.style, n.category, n.label, (n==graph.root), n.__dict__)
        
    for e in graph.edges:
        if g.has_key(e.node1.id) and \
           g.has_key(e.node2.id):
            g.add_edge(e.node1.id, e.node2.id, e.weight, e.length, e.label, e.__dict__)
    
    # Should we look for shortest paths between nodes here?
    
    return g