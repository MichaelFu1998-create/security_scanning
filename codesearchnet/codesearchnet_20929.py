def cookie_dump(key, value='', max_age=None, expires=None, path='/',
                domain=None, secure=False, httponly=False):
    """
    :rtype: ``Cookie.SimpleCookie``
    """
    cookie = SimpleCookie()
    cookie[key] = value
    for attr in ('max_age', 'expires', 'path', 'domain',
                 'secure', 'httponly'):
        attr_key = attr.replace('_', '-')
        attr_value = locals()[attr]
        if attr_value:
            cookie[key][attr_key] = attr_value
    return cookie