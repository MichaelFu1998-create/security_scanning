def proxy_factory(BaseSchema, label, ProxiedClass, get_key):
    """Create a proxy to a class instance stored in ``proxies``.

    :param class BaseSchema: Base schema (e.g. ``StoredObject``)
    :param str label: Name of class variable to set
    :param class ProxiedClass: Class to get or create
    :param function get_key: Extension-specific key function; may return e.g.
        the current Flask request

    """
    def local():
        key = get_key()
        try:
            return proxies[BaseSchema][label][key]
        except KeyError:
            proxies[BaseSchema][label][key] = ProxiedClass()
            return proxies[BaseSchema][label][key]
    return LocalProxy(local)