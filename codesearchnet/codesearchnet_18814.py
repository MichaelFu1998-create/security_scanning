def _get_children_by_tag_name(node, name):
    """Retrieve all children from node 'node' with name 'name'."""
    try:
        return [child for child in node.childNodes if child.nodeName == name]
    except TypeError:
        return []