def remove(name_or_path):
    '''Remove an environment or module

    :param name_or_path: name or path to environment or module
    '''

    r = resolve(name_or_path)
    r.resolved[0].remove()

    EnvironmentCache.discard(r.resolved[0])
    EnvironmentCache.save()