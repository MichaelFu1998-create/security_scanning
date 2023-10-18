def _dict2dict(adj_dict):
    """Takes a dictionary based representation of an adjacency list
    and returns a dict of dicts based representation.
    """
    item = adj_dict.popitem()
    adj_dict[item[0]] = item[1]
    if not isinstance(item[1], dict):
        new_dict = {}
        for key, value in adj_dict.items():
            new_dict[key] = {v: {} for v in value}

        adj_dict = new_dict
    return adj_dict