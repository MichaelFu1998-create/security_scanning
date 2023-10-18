def depth_first_search(root, visit=lambda node: False, traversable=lambda node, edge: True):

    """ Simple, multi-purpose depth-first search.
    
    Visits all the nodes connected to the root, depth-first.
    The visit function is called on each node.
    Recursion will stop if it returns True, and ubsequently dfs() will return True.
    The traversable function takes the current node and edge,
    and returns True if we are allowed to follow this connection to the next node.
    For example, the traversable for directed edges is follows:
    lambda node, edge: node == edge.node1
    
    Note: node._visited is expected to be False for all nodes.
    
    """

    stop = visit(root)
    root._visited = True
    for node in root.links:
        if stop: return True
        if not traversable(root, root.links.edge(node)): continue
        if not node._visited:
            stop = depth_first_search(node, visit, traversable)
    return stop