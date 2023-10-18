def active_env_module_resolver(resolver, path):
    '''Resolves modules in currently active environment.'''

    from .api import get_active_env

    env = get_active_env()
    if not env:
        raise ResolveError

    mod = env.get_module(path)
    if not mod:
        raise ResolveError

    return mod