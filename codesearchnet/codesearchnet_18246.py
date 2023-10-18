def with_proxies(proxy_map, get_key):
    """Class decorator factory; adds proxy class variables to target class.

    :param dict proxy_map: Mapping between class variable labels and proxied
        classes
    :param function get_key: Extension-specific key function; may return e.g.
        the current Flask request

    """
    def wrapper(cls):
        for label, ProxiedClass in six.iteritems(proxy_map):
            proxy = proxy_factory(cls, label, ProxiedClass, get_key)
            setattr(cls, label, proxy)
        return cls
    return wrapper