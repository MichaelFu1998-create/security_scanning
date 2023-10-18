def textwidth(str):
    
    """textwidth() reports incorrectly when lineheight() is smaller than 1.0
    """
    
    try: from web import _ctx
    except: pass
    
    l = _ctx.lineheight()
    _ctx.lineheight(1)
    w = _ctx.textwidth(str)
    _ctx.lineheight(l)
    
    return w