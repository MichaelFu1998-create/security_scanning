def hashFile(handle, want_hex=False, limit=None, chunk_size=CHUNK_SIZE):
    """Generate a hash from a potentially long file.
    Digesting will obey :const:`CHUNK_SIZE` to conserve memory.

    :param handle: A file-like object or path to hash from.
    :param want_hex: If ``True``, returned hash will be hex-encoded.
    :type want_hex: :class:`~__builtins__.bool`

    :param limit: Maximum number of bytes to read (rounded up to a multiple of
        ``CHUNK_SIZE``)
    :type limit: :class:`~__builtins__.int`

    :param chunk_size: Size of :meth:`~__builtins__.file.read` operations
        in bytes.
    :type chunk_size: :class:`~__builtins__.int`


    :rtype: :class:`~__builtins__.str`
    :returns: A binary or hex-encoded SHA1 hash.

    .. note:: It is your responsibility to close any file-like objects you pass
        in
    """
    fhash, read = hashlib.sha1(), 0
    if isinstance(handle, basestring):
        handle = file(handle, 'rb')

    if limit:
        chunk_size = min(chunk_size, limit)

    # Chunked digest generation (conserve memory)
    for block in iter(lambda: handle.read(chunk_size), ''):
        fhash.update(block)
        read += chunk_size
        if 0 < limit <= read:
            break

    return want_hex and fhash.hexdigest() or fhash.digest()