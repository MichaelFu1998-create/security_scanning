def iter_dict_differences(a, b):
    """
    Returns a generator yielding all the keys that have values that differ between each dictionary.
    """
    common_keys = set(a).union(b)
    for k in common_keys:
        a_value = a.get(k)
        b_value = b.get(k)
        if a_value != b_value:
            yield k, (a_value, b_value)