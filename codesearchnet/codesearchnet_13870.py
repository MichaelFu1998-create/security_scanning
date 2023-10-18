def path(s, graph, path):

    """ Visualization of a shortest path between two nodes.
    """

    def end(n):
        r = n.r * 0.35
        s._ctx.oval(n.x-r, n.y-r, r*2, r*2)

    if path and len(path) > 1 and s.stroke:

        s._ctx.nofill()
        s._ctx.stroke(
            s.stroke.r,
            s.stroke.g,
            s.stroke.b,
            s.stroke.a
        )
        if s.name != DEFAULT:
            s._ctx.strokewidth(s.strokewidth)
        else:
            s._ctx.strokewidth(s.strokewidth*2)
            
        first = True
        for id in path:
            n = graph[id]
            if first:
                first = False
                s._ctx.beginpath(n.x, n.y)
                end(n)
            else:
                s._ctx.lineto(n.x, n.y)
        s._ctx.endpath()
        end(n)