def _time_independent_equals(a, b):
    '''
    This compares two values in constant time.

    Taken from tornado:

    https://github.com/tornadoweb/tornado/blob/
    d4eb8eb4eb5cc9a6677e9116ef84ded8efba8859/tornado/web.py#L3060

    '''
    if len(a) != len(b):
        return False
    result = 0
    if isinstance(a[0], int):  # python3 byte strings
        for x, y in zip(a, b):
            result |= x ^ y
    else:  # python2
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
    return result == 0