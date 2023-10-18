def redirect_resolver(resolver, path):
    '''Resolves environment from .cpenv file...recursively walks up the tree
    in attempt to find a .cpenv file'''

    if not os.path.exists(path):
        raise ResolveError

    if os.path.isfile(path):
        path = os.path.dirname(path)

    for root, _, _ in walk_up(path):
        if is_redirecting(root):
            env_paths = redirect_to_env_paths(unipath(root, '.cpenv'))
            r = Resolver(*env_paths)
            return r.resolve()

    raise ResolveError