def clique(graph, id):
    
    """ Returns the largest possible clique for the node with given id.
    """
    
    clique = [id]
    for n in graph.nodes:
        friend = True
        for id in clique:
            if n.id == id or graph.edge(n.id, id) == None:
                friend = False
                break
        if friend:
            clique.append(n.id)
    
    return clique