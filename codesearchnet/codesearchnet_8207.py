def update(desc, other=None, **kwds):
    """Update sections in a Project description"""
    other = other and _as_dict(other) or {}
    for i in other, kwds:
        for k, v in i.items():
            if isinstance(v, dict):
                # Only for dicts, merge instead of overwriting
                old_v = desc[k]
                for k2, v2 in v.items():
                    if v2 is None:
                        old_v.pop(k2, None)
                    else:
                        old_v[k2] = v2
            else:
                set_one(desc, k, v)