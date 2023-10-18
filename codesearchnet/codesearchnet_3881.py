def _hashable_sequence(data, types=True):
    r"""
    Extracts the sequence of bytes that would be hashed by hash_data

    Example:
        >>> data = [2, (3, 4)]
        >>> result1 = (b''.join(_hashable_sequence(data, types=False)))
        >>> result2 = (b''.join(_hashable_sequence(data, types=True)))
        >>> assert result1 == b'_[_\x02_,__[_\x03_,_\x04_,__]__]_'
        >>> assert result2 == b'_[_INT\x02_,__[_INT\x03_,_INT\x04_,__]__]_'
    """
    hasher = _HashTracer()
    _update_hasher(hasher, data, types=types)
    return hasher.sequence