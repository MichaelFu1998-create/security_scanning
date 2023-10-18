def lrucache(func, size):
    """
    A simple implementation of a least recently used (LRU) cache.
    Memoizes the recent calls of a computationally intensive function.

    Parameters
    ----------
    func : function
        Must be unary (takes a single argument)

    size : int
        The size of the cache (number of previous calls to store)
    """

    if size == 0:
        return func
    elif size < 0:
        raise ValueError("size argument must be a positive integer")

    # this only works for unary functions
    if not is_arity(1, func):
        raise ValueError("The function must be unary (take a single argument)")

    # initialize the cache
    cache = OrderedDict()

    def wrapper(x):
        if not(type(x) is np.ndarray):
            raise ValueError("Input must be an ndarray")

        # hash the input, using tostring for small and repr for large arrays
        if x.size <= 1e4:
            key = hash(x.tostring())
        else:
            key = hash(repr(x))

        # if the key is not in the cache, evalute the function
        if key not in cache:

            # clear space if necessary (keeps the most recent keys)
            if len(cache) >= size:
                cache.popitem(last=False)

            # store the new value in the cache
            cache[key] = func(x)

        return cache[key]

    return wrapper