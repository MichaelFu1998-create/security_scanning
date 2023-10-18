def filter_dict(d, exclude):
    """Return a new dict with specified keys excluded from the origional dict

    Args:
        d (dict): origional dict
        exclude (list): The keys that are excluded
    """
    ret = {}
    for key, value in d.items():
        if key not in exclude:
            ret.update({key: value})
    return ret