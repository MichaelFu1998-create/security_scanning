def get_all_text(node):
    """Recursively extract all text from node."""
    if node.nodeType == node.TEXT_NODE:
        return node.data
    else:
        text_string = ""
        for child_node in node.childNodes:
            text_string += get_all_text(child_node)
        return text_string