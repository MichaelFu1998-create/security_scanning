def module_resolver(resolver, path):
    '''Resolves module in previously resolved environment.'''

    if resolver.resolved:

        if isinstance(resolver.resolved[0], VirtualEnvironment):
            env = resolver.resolved[0]
            mod = env.get_module(path)

            if mod:
                return mod

    raise ResolveError