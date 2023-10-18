def edges(s, edges, alpha=1.0, weighted=False, directed=False):
    
    """ Visualization of the edges in a network.
    """
    
    p = s._ctx.BezierPath()
    
    if directed and s.stroke: 
        pd = s._ctx.BezierPath()           
    if weighted and s.fill: 
        pw = [s._ctx.BezierPath() for i in range(11)]
    
    # Draw the edges in a single BezierPath for speed.
    # Weighted edges are divided into ten BezierPaths,
    # depending on their weight rounded between 0 and 10.
    if len(edges) == 0: return
    for e in edges:
        try:  s2 = e.node1.graph.styles[e.node1.style]
        except: s2 = s
        if s2.edge:
            s2.edge(s2, p, e, alpha)
            if directed and s.stroke:
                s2.edge_arrow(s2, pd, e, radius=10)
            if weighted and s.fill:
                s2.edge(s2, pw[int(e.weight*10)], e, alpha)                

    s._ctx.autoclosepath(False)
    s._ctx.nofill()
    s._ctx.nostroke()

    

    # All weighted edges use the default fill.
    if weighted and s.fill:
        r = e.node1.__class__(None).r
        s._ctx.stroke(
            s.fill.r,
            s.fill.g,
            s.fill.b,
            s.fill.a * 0.65 * alpha
        )
        for w in range(1, len(pw)):
            s._ctx.strokewidth(r*w*0.1)
            s._ctx.drawpath(pw[w].copy())        

    # All edges use the default stroke.
    if s.stroke: 
        s._ctx.strokewidth(s.strokewidth)
	
        s._ctx.stroke(
            s.stroke.r, 
            s.stroke.g, 
            s.stroke.b, 
            s.stroke.a * 0.65 * alpha
        )
    
    s._ctx.drawpath(p.copy())
    
    if directed and s.stroke:
        #clr = s._ctx.stroke().copy()
	clr=s._ctx.color(
            s.stroke.r, 
            s.stroke.g, 
            s.stroke.b, 
            s.stroke.a * 0.65 * alpha
        )
		
        clr.a *= 1.3
        
	s._ctx.stroke(clr)
        
    	s._ctx.drawpath(pd.copy())
    
    for e in edges:
        try:  s2 = self.styles[e.node1.style]
        except: s2 = s
        if s2.edge_label:
            s2.edge_label(s2, e, alpha)