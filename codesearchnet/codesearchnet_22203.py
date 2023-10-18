def _setVirtualEnv():
    """Attempt to set the virtualenv activate command, if it hasn't been specified.
    """
    try:
        activate = options.virtualenv.activate_cmd
    except AttributeError:
        activate = None

    if activate is None:
        virtualenv = path(os.environ.get('VIRTUAL_ENV', ''))
        if not virtualenv:
            virtualenv = options.paved.cwd
        else:
            virtualenv = path(virtualenv)

        activate = virtualenv / 'bin' / 'activate'

        if activate.exists():
            info('Using default virtualenv at %s' % activate)
            options.setdotted('virtualenv.activate_cmd', 'source %s' % activate)