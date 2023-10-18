def _rectify_hasher(hasher):
    """
    Convert a string-based key into a hasher class

    Notes:
        In terms of speed on 64bit systems, sha1 is the fastest followed by md5
        and sha512. The slowest algorithm is sha256. If xxhash is installed
        the fastest algorithm is xxh64.

    Example:
        >>> assert _rectify_hasher(NoParam) is DEFAULT_HASHER
        >>> assert _rectify_hasher('sha1') is hashlib.sha1
        >>> assert _rectify_hasher('sha256') is hashlib.sha256
        >>> assert _rectify_hasher('sha512') is hashlib.sha512
        >>> assert _rectify_hasher('md5') is hashlib.md5
        >>> assert _rectify_hasher(hashlib.sha1) is hashlib.sha1
        >>> assert _rectify_hasher(hashlib.sha1())().name == 'sha1'
        >>> import pytest
        >>> assert pytest.raises(KeyError, _rectify_hasher, '42')
        >>> #assert pytest.raises(TypeError, _rectify_hasher, object)
        >>> if xxhash:
        >>>     assert _rectify_hasher('xxh64') is xxhash.xxh64
        >>>     assert _rectify_hasher('xxh32') is xxhash.xxh32
    """
    if xxhash is not None:  # pragma: nobranch
        if hasher in {'xxh32', 'xx32', 'xxhash'}:
            return xxhash.xxh32
        if hasher in {'xxh64', 'xx64'}:
            return xxhash.xxh64

    if hasher is NoParam or hasher == 'default':
        hasher = DEFAULT_HASHER
    elif isinstance(hasher, six.string_types):
        if hasher not in hashlib.algorithms_available:
            raise KeyError('unknown hasher: {}'.format(hasher))
        else:
            hasher = getattr(hashlib, hasher)
    elif isinstance(hasher, HASH):
        # by default the result of this function is a class we will make an
        # instance of, if we already have an instance, wrap it in a callable
        # so the external syntax does not need to change.
        return lambda: hasher
    return hasher