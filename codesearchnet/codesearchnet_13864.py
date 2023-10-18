def graph_traffic(s, node, alpha=1.0):
    
    """ Visualization of traffic-intensive nodes (based on their centrality).
    """
    
    r = node.__class__(None).r
    r += (node.weight+0.5) * r * 5
    s._ctx.nostroke()
    if s.traffic:
        s._ctx.fill(
            s.traffic.r, 
            s.traffic.g, 
            s.traffic.b, 
            s.traffic.a * alpha
        )
        s._ctx.oval(node.x-r, node.y-r, r*2, r*2)