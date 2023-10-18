def _remove_pkcs1v15_padding(key_length, data, operation):
    """
    Removes PKCS#1 v1.5 padding from a message using constant time operations

    :param key_length:
        An integer of the number of bytes in the key

    :param data:
        A byte string to unpad

    :param operation:
        A unicode string of "decrypting" or "verifying"

    :return:
        The unpadded data as a byte string
    """

    if operation == 'decrypting':
        second_byte = 2
    else:
        second_byte = 1

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

    if len(data) != key_length:
        raise ValueError('Error %s' % operation)

    error = 0
    trash = 0
    padding_end = 0

    # Uses bitwise operations on an error variable and another trash variable
    # to perform constant time error checking/token scanning on the data
    for i in range(0, len(data)):
        byte = data[i:i + 1]
        byte_num = ord(byte)

        # First byte should be \x00
        if i == 0:
            error |= byte_num

        # Second byte should be \x02 for decryption, \x01 for verification
        elif i == 1:
            error |= int((byte_num | second_byte) != second_byte)

        # Bytes 3-10 should not be \x00
        elif i < 10:
            error |= int((byte_num ^ 0) == 0)

        # Byte 11 or after that is zero is end of padding
        else:
            non_zero = byte_num | 0
            if padding_end == 0:
                if non_zero:
                    trash |= i
                else:
                    padding_end |= i
            else:
                if non_zero:
                    trash |= i
                else:
                    trash |= i

    if error != 0:
        raise ValueError('Error %s' % operation)

    return data[padding_end + 1:]