def match(v1, v2, nomatch=-1, incomparables=None, start=0):
    """
    Return a vector of the positions of (first)
    matches of its first argument in its second.

    Parameters
    ----------
    v1: array_like
        Values to be matched

    v2: array_like
        Values to be matched against

    nomatch: int
        Value to be returned in the case when
        no match is found.

    incomparables: array_like
        Values that cannot be matched. Any value in ``v1``
        matching a value in this list is assigned the nomatch
        value.
    start: int
        Type of indexing to use. Most likely 0 or 1
    """
    v2_indices = {}
    for i, x in enumerate(v2):
        if x not in v2_indices:
            v2_indices[x] = i

    v1_to_v2_map = [nomatch] * len(v1)
    skip = set(incomparables) if incomparables else set()
    for i, x in enumerate(v1):
        if x in skip:
            continue

        try:
            v1_to_v2_map[i] = v2_indices[x] + start
        except KeyError:
            pass

    return v1_to_v2_map