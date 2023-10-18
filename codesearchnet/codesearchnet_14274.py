def add_color_info(e, path):
    
    """ Expand the path with color information.
    
    Attempts to extract fill and stroke colors
    from the element and adds it to path attributes.
    
    """
    
    _ctx.colormode(RGB, 1.0)
    
    def _color(hex, alpha=1.0):
        if hex == "none": return None
        n = int(hex[1:],16)
        r = (n>>16)&0xff
        g = (n>>8)&0xff
        b = n&0xff
        return _ctx.color(r/255.0, g/255.0, b/255.0, alpha)

    path.fill = (0,0,0,0)
    path.stroke = (0,0,0,0)
    path.strokewidth = 0

    # See if we can find an opacity attribute,
    # which is the color's alpha.
    alpha = get_attribute(e, "opacity", default="")
    if alpha == "":
        alpha = 1.0
    else:
        alpha = float(alpha)
    
    # Colors stored as fill="" or stroke="" attributes.
    try: path.fill = _color(get_attribute(e, "fill", default="#00000"), alpha)
    except: 
        pass
    try: path.stroke = _color(get_attribute(e, "stroke", default="none"), alpha)
    except: 
        pass
    try: path.strokewidth = float(get_attribute(e, "stroke-width", default="1"))
    except: 
        pass
    
    # Colors stored as a CSS style attribute, for example:
    # style="fill:#ff6600;stroke:#ffe600;stroke-width:0.06742057"
    style = get_attribute(e, "style", default="").split(";")
    for s in style:
        try:
            if s.startswith("fill:"):
                path.fill = _color(s.replace("fill:", ""))
            elif s.startswith("stroke:"):
                path.stroke = _color(s.replace("stroke:", ""))
            elif s.startswith("stroke-width:"):
                path.strokewidth = float(s.replace("stroke-width:", ""))
        except:
            pass    

    # A path with beginning and ending coordinate
    # at the same location is considered closed.
    # Unless it contains a MOVETO somewhere in the middle.
    path.closed = False
    if path[0].x == path[len(path)-1].x and \
       path[0].y == path[len(path)-1].y: 
        path.closed = True
    for i in range(1,-1):
        if path[i].cmd == MOVETO:
            path.closed = False
        
    return path