def intersection(l1, l2):
    '''Returns intersection of two lists.  Assumes the lists are sorted by start positions'''
    if len(l1) == 0 or len(l2) == 0:
        return []

    out = []
    l2_pos = 0

    for l in l1:
        while l2_pos < len(l2) and l2[l2_pos].end < l.start:
            l2_pos += 1

        if l2_pos == len(l2):
            break

        while l2_pos < len(l2) and l.intersects(l2[l2_pos]):
            out.append(l.intersection(l2[l2_pos]))
            l2_pos += 1

        l2_pos = max(0, l2_pos - 1)

    return out