def get_environments():
    '''Returns a list of all known virtual environments as
    :class:`VirtualEnvironment` instances. This includes those in CPENV_HOME
    and any others that are cached(created by the current user or activated
    once by full path.)
    '''

    environments = set()

    cwd = os.getcwd()
    for d in os.listdir(cwd):

        if d == 'environment.yml':
            environments.add(VirtualEnvironment(cwd))
            continue

        path = unipath(cwd, d)
        if utils.is_environment(path):
            environments.add(VirtualEnvironment(path))

    home = get_home_path()
    for d in os.listdir(home):

        path = unipath(home, d)
        if utils.is_environment(path):
            environments.add(VirtualEnvironment(path))

    for env in EnvironmentCache:
        environments.add(env)

    return sorted(list(environments), key=lambda x: x.name)