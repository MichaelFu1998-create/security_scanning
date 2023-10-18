def get_cache_key(prefix, *args, **kwargs):
    """
    Calculates cache key based on `args` and `kwargs`.
    `args` and `kwargs` must be instances of hashable types.
    """
    hash_args_kwargs = hash(tuple(kwargs.iteritems()) + args)
    return '{}_{}'.format(prefix, hash_args_kwargs)