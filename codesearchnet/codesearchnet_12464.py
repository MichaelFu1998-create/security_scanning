def reapply_all(ast_node, lib2to3_node):
    """Reapplies the typed_ast node into the lib2to3 tree.

    Also does post-processing. This is done in reverse order to enable placing
    TypeVars and aliases that depend on one another.
    """
    late_processing = reapply(ast_node, lib2to3_node)
    for lazy_func in reversed(late_processing):
        lazy_func()