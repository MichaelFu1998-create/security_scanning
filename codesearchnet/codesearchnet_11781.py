def get_component_settings(prefixes=None):
    """
    Returns a subset of the env dictionary containing
    only those keys with the name prefix.
    """
    prefixes = prefixes or []
    assert isinstance(prefixes, (tuple, list)), 'Prefixes must be a sequence type, not %s.' % type(prefixes)
    data = {}
    for name in prefixes:
        name = name.lower().strip()
        for k in sorted(env):
            if k.startswith('%s_' % name):
                new_k = k[len(name)+1:]
                data[new_k] = env[k]
    return data