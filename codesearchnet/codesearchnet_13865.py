def node(s, node, alpha=1.0):

    """ Visualization of a default node.
    """

    if s.depth:
        try: colors.shadow(dx=5, dy=5, blur=10, alpha=0.5*alpha)
        except: pass
    
    s._ctx.nofill()
    s._ctx.nostroke()
    if s.fill:
        s._ctx.fill(
            s.fill.r, 
            s.fill.g, 
            s.fill.b, 
            s.fill.a * alpha
        )
    if s.stroke: 
        s._ctx.strokewidth(s.strokewidth)
        s._ctx.stroke(
            s.stroke.r, 
            s.stroke.g, 
            s.stroke.b, 
            s.stroke.a * alpha * 3
        )
    r = node.r
    s._ctx.oval(node.x-r, node.y-r, r*2, r*2)