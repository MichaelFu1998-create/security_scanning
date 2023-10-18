def memoize_property(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent accesses
    is returned, preventing the need to call the getter any more.

    This decorator can either be used by itself or by decorating another
    property. In either case the method will always become a property.

    Notes:
        implementation is a modified version of [1].

    References:
        ..[1] https://github.com/estebistec/python-memoized-property

    CommandLine:
        xdoctest -m ubelt.util_memoize memoize_property

    Example:
        >>> class C(object):
        ...     load_name_count = 0
        ...     @memoize_property
        ...     def name(self):
        ...         "name's docstring"
        ...         self.load_name_count += 1
        ...         return "the name"
        ...     @memoize_property
        ...     @property
        ...     def another_name(self):
        ...         "name's docstring"
        ...         self.load_name_count += 1
        ...         return "the name"
        >>> c = C()
        >>> c.load_name_count
        0
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
        >>> c.another_name
    """
    # Unwrap any existing property decorator
    while hasattr(fget, 'fget'):
        fget = fget.fget

    attr_name = '_' + fget.__name__

    @functools.wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)