def to_int(data):
    """
    :params data: proquint
    :returns: proquint decoded into an integer
    :type data: string
    :rtype: int
    """
    if not isinstance(data, basestring):
        raise TypeError('Input must be string')

    res = 0
    for part in data.split('-'):
        if len(part) != 5:
            raise ValueError('Malformed proquint')
        for j in range(5):
            try:
                if not j % 2:
                    res <<= 4
                    res |= CONSONANTS.index(part[j])
                else:
                    res <<= 2
                    res |= VOWELS.index(part[j])
            except ValueError:
                raise ValueError('Unknown character \'{!s}\' in proquint'.format(part[j]))
    return res