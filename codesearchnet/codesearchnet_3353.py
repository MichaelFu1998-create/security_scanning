def rlp_encode(item):
    r""" Recursive Length Prefix Encoding
        :param item: the object to encode, either a string, bytes, bytearray, int, long, or sequence

    https://github.com/ethereum/wiki/wiki/RLP

    >>> rlp_encode('dog')
    b'\x83dog'

    >>> rlp_encode([ 'cat', 'dog' ])
    b'\xc8\x83cat\x83dog'

    >>> rlp_encode('')
    b'\x80'

    >>> rlp_encode([])
    b'\xc0'

    >>> rlp_encode(0)
    b'\x80'

    >>> rlp_encode('\x00')
    b'\x00'

    >>> rlp_encode(15)
    b'\x0f'

    >>> rlp_encode(1024)
    b'\x82\x04\x00'

    >>> rlp_encode([ [], [[]], [ [], [[]] ] ])
    b'\xc7\xc0\xc1\xc0\xc3\xc0\xc1\xc0'

    """
    if item is None or item == 0:
        ret = b'\x80'
    elif isinstance(item, str):
        ret = rlp_encode(item.encode('utf8'))
    elif isinstance(item, (bytearray, bytes)):
        if len(item) == 1 and item[0] < 0x80:
            # For a single byte whose value is in the [0x00, 0x7f] range, that byte is its own RLP encoding.
            ret = item
        else:
            ret = encode_length(len(item), 0x80) + item
    elif isinstance(item, collections.abc.Sequence):
        output = b''.join(map(rlp_encode, item))
        ret = encode_length(len(output), 0xC0) + output
    elif isinstance(item, int):
        ret = rlp_encode(int_to_bytes(item))
    else:
        raise Exception("Cannot encode object of type %s" % type(item).__name__)
    return ret