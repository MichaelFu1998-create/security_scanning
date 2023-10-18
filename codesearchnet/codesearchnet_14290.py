def usable_class_name(node):
    """Make a reasonable class name for a class node."""
    name = node.qname()
    for prefix in ["__builtin__.", "builtins.", "."]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name