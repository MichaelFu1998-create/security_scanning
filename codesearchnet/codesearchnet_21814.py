def cache_resolver(resolver, path):
    '''Resolves VirtualEnvironments in EnvironmentCache'''

    env = resolver.cache.find(path)
    if env:
        return env

    raise ResolveError