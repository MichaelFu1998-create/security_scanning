def parse_transform(e, path):
    
    """ Transform the path according to a defined matrix.
    
    Attempts to extract a transform="matrix()|translate()" attribute.
    Transforms the path accordingly.
    
    """
    
    t = get_attribute(e, "transform", default="")
    
    for mode in ("matrix", "translate"):
        if t.startswith(mode):
            v = t.replace(mode, "").lstrip("(").rstrip(")")
            v = v.replace(", ", ",").replace(" ", ",")
            v = [float(x) for x in v.split(",")]
            from nodebox.graphics import Transform
            t = Transform()            
            if mode == "matrix":
                t._set_matrix(v)
            elif mode == "translate":
                t.translate(*v)
            path = t.transformBezierPath(path)
            break

    # Transformations can also be defined as <g transform="matrix()"><path /><g>
    # instead of <g><path transform="matrix() /></g>.
    e = e.parentNode
    if e and e.tagName == "g":
        path = parse_transform(e, path)
        
    return path