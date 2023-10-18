def dict_merge(a, b, k):
    """
    Merge two dictionary lists
    :param a: original list
    :param b: alternative list, element will replace the one in original list with same key
    :param k: key
    :return: the merged list
    """
    c = a.copy()
    for j in range(len(b)):
        flag = False
        for i in range(len(c)):
            if c[i][k] == b[j][k]:
                c[i] = b[j].copy()
                flag = True
        if not flag:
            c.append(b[j].copy())
    return c