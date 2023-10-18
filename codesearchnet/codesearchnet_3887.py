def hash_file(fpath, blocksize=65536, stride=1, hasher=NoParam,
              hashlen=NoParam, base=NoParam):
    """
    Hashes the data in a file on disk.

    Args:
        fpath (PathLike):  file path string

        blocksize (int): 2 ** 16. Affects speed of reading file

        stride (int): strides > 1 skip data to hash, useful for faster
                      hashing, but less accurate, also makes hash dependant on
                      blocksize.

        hasher (HASH): hash algorithm from hashlib, defaults to `sha512`.

        hashlen (int): maximum number of symbols in the returned hash. If
            not specified, all are returned.

        base (list, str): list of symbols or shorthand key. Valid keys are
            'abc', 'hex', and 'dec'. Defaults to 'hex'.

    Notes:
        For better hashes keep stride = 1
        For faster hashes set stride > 1
        blocksize matters when stride > 1

    References:
        http://stackoverflow.com/questions/3431825/md5-checksum-of-a-file
        http://stackoverflow.com/questions/5001893/when-to-use-sha-1-vs-sha-2

    Example:
        >>> import ubelt as ub
        >>> from os.path import join
        >>> fpath = join(ub.ensure_app_cache_dir('ubelt'), 'tmp.txt')
        >>> ub.writeto(fpath, 'foobar')
        >>> print(ub.hash_file(fpath, hasher='sha1', base='hex'))
        8843d7f92416211de9ebb963ff4ce28125932878

    Example:
        >>> import ubelt as ub
        >>> from os.path import join
        >>> fpath = ub.touch(join(ub.ensure_app_cache_dir('ubelt'), 'empty_file'))
        >>> # Test that the output is the same as sha1sum
        >>> if ub.find_exe('sha1sum'):
        >>>     want = ub.cmd(['sha1sum', fpath], verbose=2)['out'].split(' ')[0]
        >>>     got = ub.hash_file(fpath, hasher='sha1')
        >>>     print('want = {!r}'.format(want))
        >>>     print('got = {!r}'.format(got))
        >>>     assert want.endswith(got)
        >>> # Do the same for sha512 sum and md5sum
        >>> if ub.find_exe('sha512sum'):
        >>>     want = ub.cmd(['sha512sum', fpath], verbose=2)['out'].split(' ')[0]
        >>>     got = ub.hash_file(fpath, hasher='sha512')
        >>>     print('want = {!r}'.format(want))
        >>>     print('got = {!r}'.format(got))
        >>>     assert want.endswith(got)
        >>> if ub.find_exe('md5sum'):
        >>>     want = ub.cmd(['md5sum', fpath], verbose=2)['out'].split(' ')[0]
        >>>     got = ub.hash_file(fpath, hasher='md5')
        >>>     print('want = {!r}'.format(want))
        >>>     print('got = {!r}'.format(got))
        >>>     assert want.endswith(got)
    """
    base = _rectify_base(base)
    hashlen = _rectify_hashlen(hashlen)
    hasher = _rectify_hasher(hasher)()
    with open(fpath, 'rb') as file:
        buf = file.read(blocksize)
        if stride > 1:
            # skip blocks when stride is greater than 1
            while len(buf) > 0:
                hasher.update(buf)
                file.seek(blocksize * (stride - 1), 1)
                buf = file.read(blocksize)
        else:
            # otherwise hash the entire file
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(blocksize)
    # Get the hashed representation
    text = _digest_hasher(hasher, hashlen, base)
    return text