def merge_dicts(base, changes):
    """Merge b into a recursively, without overwriting values.

    :param base: the dict that will be altered.
    :param changes: changes to update base.
    """
    for k, v in changes.items():
        if isinstance(v, dict):
            merge_dicts(base.setdefault(k, {}), v)
        else:
            base.setdefault(k, v)