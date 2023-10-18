def from_int(data):
    """
    :params data: integer
    :returns: proquint made from input data
    :type data: int
    :rtype: string
    """
    if not isinstance(data, int) and not isinstance(data, long):
        raise TypeError('Input must be integer')

    res = []
    while data > 0 or not res:
        for j in range(5):
            if not j % 2:
                res += CONSONANTS[(data & 0xf)]
                data >>= 4
            else:
                res += VOWELS[(data & 0x3)]
                data >>= 2
        if data > 0:
            res += '-'
    res.reverse()
    return ''.join(res)