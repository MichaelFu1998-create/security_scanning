def dict_merge(base, top):
    """Recursively merge two dictionaries, with the elements from `top`
    taking precedence over elements from `top`.

    Returns
    -------
    out : dict
        A new dict, containing the merged records.
    """
    out = dict(top)
    for key in base:
        if key in top:
            if isinstance(base[key], dict) and isinstance(top[key], dict):
                out[key] = dict_merge(base[key], top[key])
        else:
            out[key] = base[key]
    return out