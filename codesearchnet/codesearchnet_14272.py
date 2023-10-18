def parse_node(node, paths=[], ignore=["pattern"]):
    
    """ Recurse the node tree and find drawable tags.
    
    Recures all the children in the node.
    If a child is something we can draw,
    a line, rect, oval or path,
    parse it to a PathElement drawable with drawpath()
    
    """
    
    # Ignore paths in Illustrator pattern swatches etc.
    if node.nodeType == node.ELEMENT_NODE and node.tagName in ignore: 
        return []
    
    if node.hasChildNodes():
        for child in node.childNodes:
            paths = parse_node(child, paths)
    
    if node.nodeType == node.ELEMENT_NODE:
        
        if node.tagName == "line":
            paths.append(parse_line(node))
        elif node.tagName == "rect":
            paths.append(parse_rect(node))
        elif node.tagName == "circle":
            paths.append(parse_circle(node))
        elif node.tagName == "ellipse":
            paths.append(parse_oval(node))
        elif node.tagName == "polygon":
            paths.append(parse_polygon(node))
        elif node.tagName == "polyline":
            paths.append(parse_polygon(node))
        elif node.tagName == "path":
            paths.append(parse_path(node))
            
        if node.tagName in ("line", "rect", "circle", "ellipse", "polygon", "polyline", "path"):
            paths[-1] = parse_transform(node, paths[-1])
            paths[-1] = add_color_info(node, paths[-1])
    
    return paths