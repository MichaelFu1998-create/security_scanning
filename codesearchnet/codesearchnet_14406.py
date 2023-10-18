def get(name, default=None, allow_default=True):
    """ Shortcut method for getting a setting value.

        :param str name: Setting key name.
        :param default: Default value of setting if it's not explicitly
                        set. Defaults to `None`
        :param bool allow_default: If true, use the parameter default as
                        default if the key is not set, else raise
                        :exc:`KeyError`.  Defaults to `None`
        :raises: :exc:`KeyError` if allow_default is false and the setting is
                 not set.
    """
    return Config().get(name, default, allow_default=allow_default)