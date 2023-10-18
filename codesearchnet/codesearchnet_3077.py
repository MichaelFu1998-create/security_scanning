def is_valid_lval(t):
    """Checks whether t is valid JS identifier name (no keyword like var, function, if etc)
    Also returns false on internal"""
    if not is_internal(t) and is_lval(t) and t not in RESERVED_NAMES:
        return True
    return False