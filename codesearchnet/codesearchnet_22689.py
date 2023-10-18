def getTextFromNode(node):
    """
    Scans through all children of node and gathers the
    text. If node has non-text child-nodes then
    NotTextNodeError is raised.
    """
    t = ""
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            t += n.nodeValue
        else:
            raise NotTextNodeError
    return t