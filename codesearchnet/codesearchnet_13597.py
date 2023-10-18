def shuffle_srv(records):
    """Randomly reorder SRV records using their weights.

    :Parameters:
        - `records`: SRV records to shuffle.
    :Types:
        - `records`: sequence of :dns:`dns.rdtypes.IN.SRV`

    :return: reordered records.
    :returntype: `list` of :dns:`dns.rdtypes.IN.SRV`"""
    if not records:
        return []
    ret = []
    while len(records) > 1:
        weight_sum = 0
        for rrecord in records:
            weight_sum += rrecord.weight + 0.1
        thres = random.random() * weight_sum
        weight_sum = 0
        for rrecord in records:
            weight_sum += rrecord.weight + 0.1
            if thres < weight_sum:
                records.remove(rrecord)
                ret.append(rrecord)
                break
    ret.append(records[0])
    return ret