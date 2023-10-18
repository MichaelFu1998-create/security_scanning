def get(vals, key, default_val=None):
    """
    Returns a dictionary value
    """
    val = vals
    for part in key.split('.'):
        if isinstance(val, dict):
            val = val.get(part, None)
            if val is None:
                return default_val
        else:
            return default_val
    return val