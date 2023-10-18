def cached_property(f):
    """Similar to `@property` but it calls the function just once and caches
    the result.  The object has to can have ``__cache__`` attribute.

    If you define `__slots__` for optimization, the metaclass should be a
    :class:`CacheMeta`.

    """
    @property
    @functools.wraps(f)
    def wrapped(self, name=f.__name__):
        try:
            cache = self.__cache__
        except AttributeError:
            self.__cache__ = cache = {}
        try:
            return cache[name]
        except KeyError:
            cache[name] = rv = f(self)
            return rv
    return wrapped