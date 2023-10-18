def edge(s, path, edge, alpha=1.0):
    
    """ Visualization of a single edge between two nodes.
    """
    
    path.moveto(edge.node1.x, edge.node1.y)
    if edge.node2.style == BACK:
        path.curveto(
            edge.node1.x,
            edge.node2.y,
            edge.node2.x,
            edge.node2.y,
            edge.node2.x,
            edge.node2.y,
        )        
    else:
        path.lineto(
            edge.node2.x, 
            edge.node2.y
        )