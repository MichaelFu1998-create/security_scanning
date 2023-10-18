def path_resolver(resolver, path):
    '''Resolves VirtualEnvironments with a relative or absolute path'''

    path = unipath(path)

    if is_environment(path):
        return VirtualEnvironment(path)

    raise ResolveError