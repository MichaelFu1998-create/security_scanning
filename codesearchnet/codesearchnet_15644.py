def dict_top(d, k, n, reverse=False):
    """
    Return top n of a dictionary list sorted by key
    :param d: dictionary list
    :param k: key
    :param n: top n
    :param reverse: whether the value should be reversed
    :return: top n of the sorted dictionary list
    """
    h = list()
    for i in range(len(d)):
        heappush(h, (-d[i][k] if reverse else d[i][k], i))
    r = list()
    while len(r) < n and len(h) > 0:
        _, i = heappop(h)
        r.append(d[i].copy())
    return r