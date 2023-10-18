def hash_data(data, hasher=NoParam, base=NoParam, types=False,
              hashlen=NoParam, convert=False):
    """
    Get a unique hash depending on the state of the data.

    Args:
        data (object):
            Any sort of loosely organized data

        hasher (str or HASHER):
            Hash algorithm from hashlib, defaults to `sha512`.

        base (str or List[str]):
            Shorthand key or a list of symbols.  Valid keys are: 'abc', 'hex',
            and 'dec'. Defaults to 'hex'.

        types (bool):
            If True data types are included in the hash, otherwise only the raw
            data is hashed. Defaults to False.

        hashlen (int):
            Maximum number of symbols in the returned hash. If not specified,
            all are returned.  DEPRECATED. Use slice syntax instead.

        convert (bool, optional, default=True):
            if True, try and convert the data to json an the json is hashed
            instead. This can improve runtime in some instances, however the
            hash may differ from the case where convert=False.

    Notes:
        alphabet26 is a pretty nice base, I recommend it.
        However we default to hex because it is standard.
        This means the output of hashdata with base=sha1 will be the same as
        the output of `sha1sum`.

    Returns:
        str: text -  hash string

    Example:
        >>> import ubelt as ub
        >>> print(ub.hash_data([1, 2, (3, '4')], convert=False))
        60b758587f599663931057e6ebdf185a...
        >>> print(ub.hash_data([1, 2, (3, '4')], base='abc',  hasher='sha512')[:32])
        hsrgqvfiuxvvhcdnypivhhthmrolkzej
    """
    if convert and isinstance(data, six.string_types):  # nocover
        try:
            data = json.dumps(data)
        except TypeError as ex:
            # import warnings
            # warnings.warn('Unable to encode input as json due to: {!r}'.format(ex))
            pass

    base = _rectify_base(base)
    hashlen = _rectify_hashlen(hashlen)
    hasher = _rectify_hasher(hasher)()
    # Feed the data into the hasher
    _update_hasher(hasher, data, types=types)
    # Get the hashed representation
    text = _digest_hasher(hasher, hashlen, base)
    return text