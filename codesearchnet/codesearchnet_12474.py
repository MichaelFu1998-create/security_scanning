def flatten_some(children):
    """Generates nodes or leaves, unpacking bodies of try:except:finally: statements."""
    for node in children:
        if node.type in (syms.try_stmt, syms.suite):
            yield from flatten_some(node.children)
        else:
            yield node