def rename(blocks, scope, stype):
    """ Rename all sub-blocks moved under another
        block. (mixins)
    Args:
        lst (list): block list
        scope (object): Scope object
    """
    for p in blocks:
        if isinstance(p, stype):
            p.tokens[0].parse(scope)
            if p.tokens[1]:
                scope.push()
                scope.current = p.tokens[0]
                rename(p.tokens[1], scope, stype)
                scope.pop()