def can_dict(obj):
    """Can the *values* of a dict."""
    if istype(obj, dict):
        newobj = {}
        for k, v in iteritems(obj):
            newobj[k] = can(v)
        return newobj
    else:
        return obj