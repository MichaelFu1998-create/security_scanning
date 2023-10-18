def remove(path):
    '''Remove a cached environment. Removed paths will no longer be able to
    be activated by name'''

    r = cpenv.resolve(path)
    if isinstance(r.resolved[0], cpenv.VirtualEnvironment):
        EnvironmentCache.discard(r.resolved[0])
        EnvironmentCache.save()