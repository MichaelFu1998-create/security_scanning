def compare(left, right, compare_locs=False):
    """
    An AST comparison function. Returns ``True`` if all fields in
    ``left`` are equal to fields in ``right``; if ``compare_locs`` is
    true, all locations should match as well.
    """
    if type(left) != type(right):
        return False

    if isinstance(left, ast.AST):
        for field in left._fields:
            if not compare(getattr(left, field), getattr(right, field)):
                return False

        if compare_locs:
            for loc in left._locs:
                if getattr(left, loc) != getattr(right, loc):
                    return False

        return True
    elif isinstance(left, list):
        if len(left) != len(right):
            return False

        for left_elt, right_elt in zip(left, right):
            if not compare(left_elt, right_elt):
                return False

        return True
    else:
        return left == right