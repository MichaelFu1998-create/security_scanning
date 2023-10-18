def create(name_or_path=None, config=None):
    '''Create a virtual environment. You can pass either the name of a new
    environment to create in your CPENV_HOME directory OR specify a full path
    to create an environment outisde your CPENV_HOME.

    Create an environment in CPENV_HOME::

        >>> cpenv.create('myenv')

    Create an environment elsewhere::

        >>> cpenv.create('~/custom_location/myenv')

    :param name_or_path: Name or full path of environment
    :param config: Environment configuration including dependencies etc...
    '''

    # Get the real path of the environment
    if utils.is_system_path(name_or_path):
        path = unipath(name_or_path)
    else:
        path = unipath(get_home_path(), name_or_path)

    if os.path.exists(path):
        raise OSError('{} already exists'.format(path))

    env = VirtualEnvironment(path)
    utils.ensure_path_exists(env.path)

    if config:
        if utils.is_git_repo(config):
            Git('').clone(config, env.path)
        else:
            shutil.copy2(config, env.config_path)
    else:
        with open(env.config_path, 'w') as f:
            f.write(defaults.environment_config)

    utils.ensure_path_exists(env.hook_path)
    utils.ensure_path_exists(env.modules_path)

    env.run_hook('precreate')

    virtualenv.create_environment(env.path)
    if not utils.is_home_environment(env.path):
        EnvironmentCache.add(env)
        EnvironmentCache.save()

    try:
        env.update()
    except:
        utils.rmtree(path)
        logger.debug('Failed to update, rolling back...')
        raise
    else:
        env.run_hook('postcreate')

    return env