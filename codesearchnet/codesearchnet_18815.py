def _get_children_as_string(node):
    """Iterate through all the children of a node.

    Returns one string containing the values from all the text-nodes
    recursively.
    """
    out = []
    if node:
        for child in node:
            if child.nodeType == child.TEXT_NODE:
                out.append(child.data)
            else:
                out.append(_get_children_as_string(child.childNodes))
    return ''.join(out)