def main(*args):
    r"""Bootstrap Python projects and libraries with virtualenv and pip.

    Also check system requirements before bootstrap and run post bootstrap
    hook if any.

    :param \*args: Command line arguments list.
    """
    # Create parser, read arguments from direct input or command line
    with disable_error_handler():
        args = parse_args(args or sys.argv[1:])

    # Read current config from file and command line arguments
    config = read_config(args.config, args)
    if config is None:
        return True
    bootstrap = config[__script__]

    # Check pre-requirements
    if not check_pre_requirements(bootstrap['pre_requirements']):
        return True

    # Create virtual environment
    env_args = prepare_args(config['virtualenv'], bootstrap)
    if not create_env(
        bootstrap['env'],
        env_args,
        bootstrap['recreate'],
        bootstrap['ignore_activated'],
        bootstrap['quiet']
    ):
        # Exit if couldn't create virtual environment
        return True

    # And install library or project here
    pip_args = prepare_args(config['pip'], bootstrap)
    if not install(
        bootstrap['env'],
        bootstrap['requirements'],
        pip_args,
        bootstrap['ignore_activated'],
        bootstrap['install_dev_requirements'],
        bootstrap['quiet']
    ):
        # Exist if couldn't install requirements into venv
        return True

    # Run post-bootstrap hook
    run_hook(bootstrap['hook'], bootstrap, bootstrap['quiet'])

    # All OK!
    if not bootstrap['quiet']:
        print_message('All OK!')

    # False means everything went alright, exit code: 0
    return False