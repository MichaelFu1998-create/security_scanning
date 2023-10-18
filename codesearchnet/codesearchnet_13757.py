def groupify(function):
    """Decorator to convert a function which takes a single value and returns
    a key into one which takes a list of values and returns a dict of key-group
    mappings.

    :param function: A function which takes a value and returns a hash key.
    :type function: ``function(value) -> key``

    :rtype:
        .. parsed-literal::
            function(iterable) ->
                {key: :class:`~__builtins__.set` ([value, ...]), ...}
    """

    @wraps(function)
    def wrapper(paths, *args, **kwargs):  # pylint: disable=missing-docstring
        groups = {}

        for path in paths:
            key = function(path, *args, **kwargs)
            if key is not None:
                groups.setdefault(key, set()).add(path)

        return groups
    return wrapper