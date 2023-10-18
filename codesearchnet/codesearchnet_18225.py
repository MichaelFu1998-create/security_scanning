def has_storage(func):
    """ Ensure that self/cls contains a Storage backend. """
    @wraps(func)
    def wrapped(*args, **kwargs):
        me = args[0]
        if not hasattr(me, '_storage') or \
                not me._storage:
            raise exceptions.ImproperConfigurationError(
                'No storage backend attached to schema <{0}>.'
                    .format(me._name.upper())
            )
        return func(*args, **kwargs)
    return wrapped