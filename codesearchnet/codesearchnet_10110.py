def constant_compare(a, b):
    """
    Compares two byte strings in constant time to see if they are equal

    :param a:
        The first byte string

    :param b:
        The second byte string

    :return:
        A boolean if the two byte strings are equal
    """

    if not isinstance(a, byte_cls):
        raise TypeError(pretty_message(
            '''
            a must be a byte string, not %s
            ''',
            type_name(a)
        ))

    if not isinstance(b, byte_cls):
        raise TypeError(pretty_message(
            '''
            b must be a byte string, not %s
            ''',
            type_name(b)
        ))

    if len(a) != len(b):
        return False

    if sys.version_info < (3,):
        a = [ord(char) for char in a]
        b = [ord(char) for char in b]

    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0