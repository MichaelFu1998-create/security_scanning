def create_env(env, args, recreate=False, ignore_activated=False, quiet=False):
    """Create virtual environment.

    :param env: Virtual environment name.
    :param args: Pass given arguments to ``virtualenv`` script.
    :param recerate: Recreate virtual environment? By default: False
    :param ignore_activated:
        Ignore already activated virtual environment and create new one. By
        default: False
    :param quiet: Do not output messages into terminal. By default: False
    """
    cmd = None
    result = True

    inside_env = hasattr(sys, 'real_prefix') or os.environ.get('VIRTUAL_ENV')
    env_exists = os.path.isdir(env)

    if not quiet:
        print_message('== Step 1. Create virtual environment ==')

    if (
        recreate or (not inside_env and not env_exists)
    ) or (
        ignore_activated and not env_exists
    ):
        cmd = ('virtualenv', ) + args + (env, )

    if not cmd and not quiet:
        if inside_env:
            message = 'Working inside of virtual environment, done...'
        else:
            message = 'Virtual environment {0!r} already created, done...'
        print_message(message.format(env))

    if cmd:
        with disable_error_handler():
            result = not run_cmd(cmd, echo=not quiet)

    if not quiet:
        print_message()

    return result