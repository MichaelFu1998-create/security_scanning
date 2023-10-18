def _convert_to_hashable(data, types=True):
    r"""
    Converts `data` into a hashable byte representation if an appropriate
    hashing function is known.

    Args:
        data (object): ordered data with structure
        types (bool): include type prefixes in the hash

    Returns:
        tuple(bytes, bytes): prefix, hashable:
            a prefix hinting the original data type and the byte representation
            of `data`.

    Raises:
        TypeError : if data has no registered hash methods

    Example:
        >>> assert _convert_to_hashable(None) == (b'NULL', b'NONE')
        >>> assert _convert_to_hashable('string') == (b'TXT', b'string')
        >>> assert _convert_to_hashable(1) == (b'INT', b'\x01')
        >>> assert _convert_to_hashable(1.0) == (b'FLT', b'\x01/\x01')
        >>> assert _convert_to_hashable(_intlike[-1](1)) == (b'INT', b'\x01')
    """
    # HANDLE MOST COMMON TYPES FIRST
    if data is None:
        hashable = b'NONE'
        prefix = b'NULL'
    elif isinstance(data, six.binary_type):
        hashable = data
        prefix = b'TXT'
    elif isinstance(data, six.text_type):
        # convert unicode into bytes
        hashable = data.encode('utf-8')
        prefix = b'TXT'
    elif isinstance(data, _intlike):
        # warnings.warn('Hashing ints is slow, numpy is prefered')
        hashable = _int_to_bytes(data)
        # hashable = data.to_bytes(8, byteorder='big')
        prefix = b'INT'
    elif isinstance(data, float):
        a, b = float(data).as_integer_ratio()
        hashable = _int_to_bytes(a) + b'/' +  _int_to_bytes(b)
        prefix = b'FLT'
    else:
        # Then dynamically look up any other type
        hash_func = _HASHABLE_EXTENSIONS.lookup(data)
        prefix, hashable = hash_func(data)
    if types:
        return prefix, hashable
    else:
        return b'', hashable