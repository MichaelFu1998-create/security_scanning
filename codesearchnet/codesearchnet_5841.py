def merge_results(x, y):
    """
    Given two dicts, x and y, merge them into a new dict as a shallow copy.

    The result only differs from `x.update(y)` in the way that it handles list
    values when both x and y have list values for the same key. In which case
    the returned dictionary, z, has a value according to:
      z[key] = x[key] + z[key]

    :param x: The first dictionary
    :type x: :py:class:`dict`
    :param y: The second dictionary
    :type y: :py:class:`dict`
    :returns: The merged dictionary
    :rtype: :py:class:`dict`
    """
    z = x.copy()
    for key, value in y.items():
        if isinstance(value, list) and isinstance(z.get(key), list):
            z[key] += value
        else:
            z[key] = value
    return z