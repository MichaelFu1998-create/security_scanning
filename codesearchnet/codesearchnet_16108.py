def encrypt(base_field, key=None, ttl=None):
    """
    A decorator for creating encrypted model fields.

    :type base_field: models.Field[T]
    :param bytes key: This is an optional argument.

        Allows for specifying an instance specific encryption key.
    :param int ttl: This is an optional argument.

        The amount of time in seconds that a value can be stored for. If the
        time to live of the data has passed, it will become unreadable.
        The expired value will return an :class:`Expired` object.
    :rtype: models.Field[EncryptedMixin, T]
    """
    if not isinstance(base_field, models.Field):
        assert key is None
        assert ttl is None
        return get_encrypted_field(base_field)

    name, path, args, kwargs = base_field.deconstruct()
    kwargs.update({'key': key, 'ttl': ttl})
    return get_encrypted_field(base_field.__class__)(*args, **kwargs)