def _forbidden_attributes(obj):
    """Return the object without the forbidden attributes."""
    for key in list(obj.data.keys()):
        if key in list(obj.reserved_keys.keys()):
            obj.data.pop(key)
    return obj