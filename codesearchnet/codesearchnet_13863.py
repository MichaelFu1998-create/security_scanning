def graph_background(s):

    """ Graph background color.
    """

    if s.background == None:
        s._ctx.background(None)
    else:
        s._ctx.background(s.background)  

    if s.depth:
        try:
            clr = colors.color(s.background).darker(0.2)
            p = s._ctx.rect(0, 0, s._ctx.WIDTH, s._ctx.HEIGHT, draw=False)
            colors.gradientfill(p, clr, clr.lighter(0.35))
            colors.shadow(dx=0, dy=0, blur=2, alpha=0.935, clr=s.background)
        except:
            pass