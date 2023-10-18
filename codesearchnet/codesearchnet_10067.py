def rand_bytes(length):
    """
    Returns a number of random bytes suitable for cryptographic purposes

    :param length:
        The desired number of bytes

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string
    """

    if not isinstance(length, int_types):
        raise TypeError(pretty_message(
            '''
            length must be an integer, not %s
            ''',
            type_name(length)
        ))

    if length < 1:
        raise ValueError('length must be greater than 0')

    if length > 1024:
        raise ValueError('length must not be greater than 1024')

    buffer = buffer_from_bytes(length)
    result = Security.SecRandomCopyBytes(Security.kSecRandomDefault, length, buffer)
    if result != 0:
        raise OSError(_extract_error())

    return bytes_from_buffer(buffer)