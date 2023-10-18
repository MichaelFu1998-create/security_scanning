def _add_pkcs1v15_padding(key_length, data, operation):
    """
    Adds PKCS#1 v1.5 padding to a message

    :param key_length:
        An integer of the number of bytes in the key

    :param data:
        A byte string to unpad

    :param operation:
        A unicode string of "encrypting" or "signing"

    :return:
        The padded data as a byte string
    """

    if operation == 'encrypting':
        second_byte = b'\x02'
    else:
        second_byte = b'\x01'

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    if not isinstance(key_length, int_types):
        raise TypeError(pretty_message(
            '''
            key_length must be an integer, not %s
            ''',
            type_name(key_length)
        ))

    if key_length < 64:
        raise ValueError(pretty_message(
            '''
            key_length must be 64 or more - is %s
            ''',
            repr(key_length)
        ))

    if len(data) > key_length - 11:
        raise ValueError(pretty_message(
            '''
            data must be between 1 and %s bytes long - is %s
            ''',
            key_length - 11,
            len(data)
        ))

    required_bytes = key_length - 3 - len(data)
    padding = b''
    while required_bytes > 0:
        temp_padding = rand_bytes(required_bytes)
        # Remove null bytes since they are markers in PKCS#1 v1.5
        temp_padding = b''.join(temp_padding.split(b'\x00'))
        padding += temp_padding
        required_bytes -= len(temp_padding)

    return b'\x00' + second_byte + padding + b'\x00' + data