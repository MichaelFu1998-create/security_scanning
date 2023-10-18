def cache(func, memory, func_memory_level=None, memory_level=None,
          **kwargs):
    """ Return a joblib.Memory object.

    The memory_level determines the level above which the wrapped
    function output is cached. By specifying a numeric value for
    this level, the user can to control the amount of cache memory
    used. This function will cache the function call or not
    depending on the cache level.

    Parameters
    ----------
    func: function
        The function which output is to be cached.

    memory: instance of joblib.Memory or string
        Used to cache the function call.

    func_memory_level: int, optional
        The memory_level from which caching must be enabled for the wrapped
        function.

    memory_level: int, optional
        The memory_level used to determine if function call must
        be cached or not (if user_memory_level is equal of greater than
        func_memory_level the function is cached)

    kwargs: keyword arguments
        The keyword arguments passed to memory.cache

    Returns
    -------
    mem: joblib.MemorizedFunc
        object that wraps the function func. This object may be
        a no-op, if the requested level is lower than the value given
        to _cache()). For consistency, a joblib.Memory object is always
        returned.
    """
    verbose = kwargs.get('verbose', 0)

    # memory_level and func_memory_level must be both None or both integers.
    memory_levels = [memory_level, func_memory_level]
    both_params_integers = all(isinstance(lvl, int) for lvl in memory_levels)
    both_params_none = all(lvl is None for lvl in memory_levels)

    if not (both_params_integers or both_params_none):
        raise ValueError('Reference and user memory levels must be both None '
                         'or both integers.')

    if memory is not None and (func_memory_level is None or
                               memory_level >= func_memory_level):
        if isinstance(memory, _basestring):
            memory = Memory(cachedir=memory, verbose=verbose)
        if not isinstance(memory, MEMORY_CLASSES):
            raise TypeError("'memory' argument must be a string or a "
                            "joblib.Memory object. "
                            "%s %s was given." % (memory, type(memory)))
        if (memory.cachedir is None and memory_level is not None
                and memory_level > 1):
            warnings.warn("Caching has been enabled (memory_level = %d) "
                          "but no Memory object or path has been provided"
                          " (parameter memory). Caching deactivated for "
                          "function %s." %
                          (memory_level, func.__name__),
                          stacklevel=2)
    else:
        memory = Memory(cachedir=None, verbose=verbose)
    return _safe_cache(memory, func, **kwargs)