def _join_seq(d, k, v):
    '''Add a sequence value to env dict'''

    if k not in d:
        d[k] = list(v)

    elif isinstance(d[k], list):
        for item in v:
            if item not in d[k]:
                d[k].insert(0, item)

    elif isinstance(d[k], string_types):
        v.append(d[k])
        d[k] = v