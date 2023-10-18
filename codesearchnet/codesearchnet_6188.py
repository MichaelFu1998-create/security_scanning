def is_equal_or_child_uri(parentUri, childUri):
    """Return True, if childUri is a child of parentUri or maps to the same resource.

    Similar to <util.is_child_uri>_ ,  but this method also returns True, if parent
    equals child. ('/a/b' is considered identical with '/a/b/').
    """
    return (
        parentUri
        and childUri
        and (childUri.rstrip("/") + "/").startswith(parentUri.rstrip("/") + "/")
    )