def reorder_srv(records):
    """Reorder SRV records using their priorities and weights.

    :Parameters:
        - `records`: SRV records to shuffle.
    :Types:
        - `records`: `list` of :dns:`dns.rdtypes.IN.SRV`

    :return: reordered records.
    :returntype: `list` of :dns:`dns.rdtypes.IN.SRV`"""
    records = list(records)
    records.sort()
    ret = []
    tmp = []
    for rrecord in records:
        if not tmp or rrecord.priority == tmp[0].priority:
            tmp.append(rrecord)
            continue
        ret += shuffle_srv(tmp)
        tmp = [rrecord]
    if tmp:
        ret += shuffle_srv(tmp)
    return ret