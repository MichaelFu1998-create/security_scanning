def flatten(node, distance=1):
    
    """ Recursively lists the node and its links.
    
    Distance of 0 will return the given [node].
    Distance of 1 will return a list of the node and all its links.
    Distance of 2 will also include the linked nodes' links, etc.
    
    """
    
    # When you pass a graph it returns all the node id's in it.
    if hasattr(node, "nodes") and hasattr(node, "edges"):
        return [n.id for n in node.nodes]
    
    all = [node]
    if distance >= 1:
        for n in node.links: 
            all += n.flatten(distance-1)
    
    return unique(all)