def pip_cmd(env, cmd, ignore_activated=False, **kwargs):
    r"""Run pip command in given or activated virtual environment.

    :param env: Virtual environment name.
    :param cmd: Pip subcommand to run.
    :param ignore_activated:
        Ignore activated virtual environment and use given venv instead. By
        default: False
    :param \*\*kwargs:
        Additional keyword arguments to be passed to :func:`~run_cmd`
    """
    cmd = tuple(cmd)
    dirname = safe_path(env)

    if not ignore_activated:
        activated_env = os.environ.get('VIRTUAL_ENV')

        if hasattr(sys, 'real_prefix'):
            dirname = sys.prefix
        elif activated_env:
            dirname = activated_env

    pip_path = os.path.join(dirname, 'Scripts' if IS_WINDOWS else 'bin', 'pip')

    if kwargs.pop('return_path', False):
        return pip_path

    if not os.path.isfile(pip_path):
        raise OSError('No pip found at {0!r}'.format(pip_path))

    # Disable pip version check in tests
    if BOOTSTRAPPER_TEST_KEY in os.environ and cmd[0] == 'install':
        cmd = list(cmd)
        cmd.insert(1, '--disable-pip-version-check')
        cmd = tuple(cmd)

    with disable_error_handler():
        return run_cmd((pip_path, ) + cmd, **kwargs)