def is_child_uri(parentUri, childUri):
    """Return True, if childUri is a child of parentUri.

    This function accounts for the fact that '/a/b/c' and 'a/b/c/' are
    children of '/a/b' (and also of '/a/b/').
    Note that '/a/b/cd' is NOT a child of 'a/b/c'.
    """
    return (
        parentUri
        and childUri
        and childUri.rstrip("/").startswith(parentUri.rstrip("/") + "/")
    )