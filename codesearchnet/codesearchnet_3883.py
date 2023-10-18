def _update_hasher(hasher, data, types=True):
    """
    Converts `data` into a byte representation and calls update on the hasher
    `hashlib.HASH` algorithm.

    Args:
        hasher (HASH): instance of a hashlib algorithm
        data (object): ordered data with structure
        types (bool): include type prefixes in the hash

    Example:
        >>> hasher = hashlib.sha512()
        >>> data = [1, 2, ['a', 2, 'c']]
        >>> _update_hasher(hasher, data)
        >>> print(hasher.hexdigest()[0:8])
        e2c67675

        2ba8d82b
    """
    # Determine if the data should be hashed directly or iterated through
    if isinstance(data, (tuple, list, zip)):
        needs_iteration = True
    else:
        needs_iteration = any(check(data) for check in
                              _HASHABLE_EXTENSIONS.iterable_checks)

    if needs_iteration:
        # Denote that we are hashing over an iterable
        # Multiple structure bytes makes it harder accidently make conflicts
        SEP = b'_,_'
        ITER_PREFIX = b'_[_'
        ITER_SUFFIX = b'_]_'

        iter_ = iter(data)
        hasher.update(ITER_PREFIX)
        # first, try to nest quickly without recursive calls
        # (this works if all data in the sequence is a non-iterable)
        try:
            for item in iter_:
                prefix, hashable = _convert_to_hashable(item, types)
                binary_data = prefix + hashable + SEP
                hasher.update(binary_data)
        except TypeError:
            # need to use recursive calls
            # Update based on current item
            _update_hasher(hasher, item, types)
            for item in iter_:
                # Ensure the items have a spacer between them
                _update_hasher(hasher, item, types)
                hasher.update(SEP)
        hasher.update(ITER_SUFFIX)
    else:
        prefix, hashable = _convert_to_hashable(data, types)
        binary_data = prefix + hashable
        hasher.update(binary_data)