def eqtflength(b,a):
    """Given two list or arrays, pad with zeros the shortest array

    :param b: list or array
    :param a: list or array


    .. doctest::

        >>> from spectrum.transfer import eqtflength
        >>> a = [1,2]
        >>> b = [1,2,3,4]
        >>> a, b, = eqtflength(a,b)

    """
    d = abs(len(b)-len(a))
    if d != 0:
        if len(a) > len(b):
            try:
                b.extend([0.]*d)
            except:
                b = np.append(b, [0]*d)
        elif len(b)>len(a):
            try:
                a.extend([0.]*d)
            except:
                a = np.append(a, [0]*d)
        return b,a
    else:
        return b,a