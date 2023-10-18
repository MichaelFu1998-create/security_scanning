def draw_math(str, x, y, alpha=1.0):
    
    """ Uses mimetex to generate a GIF-image from the LaTeX equation.
    """
    
    try: from web import _ctx
    except: pass
    
    str = re.sub("</{0,1}math>", "", str.strip())
    img = mimetex.gif(str)
    w, h = _ctx.imagesize(img)
    _ctx.image(img, x, y, alpha=alpha)
    return w, h