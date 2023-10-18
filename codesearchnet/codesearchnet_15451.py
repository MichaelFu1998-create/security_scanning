def path_to_node(tree, path):
    """FST node located at the given path"""
    if path is None:
        return None

    node = tree

    for key in path:
        node = child_by_key(node, key)

    return node