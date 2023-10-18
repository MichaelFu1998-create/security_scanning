def home_resolver(resolver, path):
    '''Resolves VirtualEnvironments in CPENV_HOME'''

    from .api import get_home_path

    path = unipath(get_home_path(), path)

    if is_environment(path):
        return VirtualEnvironment(path)

    raise ResolveError