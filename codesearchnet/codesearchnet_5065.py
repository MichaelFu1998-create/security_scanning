def invoke(
    src, event_file='event.json',
    config_file='config.yaml', profile_name=None,
    verbose=False,
):
    """Simulates a call to your function.

    :param str src:
        The path to your Lambda ready project (folder must contain a valid
        config.yaml and handler module (e.g.: service.py).
    :param str alt_event:
        An optional argument to override which event file to use.
    :param bool verbose:
        Whether to print out verbose details.
    """
    # Load and parse the config file.
    path_to_config_file = os.path.join(src, config_file)
    cfg = read_cfg(path_to_config_file, profile_name)

    # Set AWS_PROFILE environment variable based on `--profile` option.
    if profile_name:
        os.environ['AWS_PROFILE'] = profile_name

    # Load environment variables from the config file into the actual
    # environment.
    env_vars = cfg.get('environment_variables')
    if env_vars:
        for key, value in env_vars.items():
            os.environ[key] = get_environment_variable_value(value)

    # Load and parse event file.
    path_to_event_file = os.path.join(src, event_file)
    event = read(path_to_event_file, loader=json.loads)

    # Tweak to allow module to import local modules
    try:
        sys.path.index(src)
    except ValueError:
        sys.path.append(src)

    handler = cfg.get('handler')
    # Inspect the handler string (<module>.<function name>) and translate it
    # into a function we can execute.
    fn = get_callable_handler_function(src, handler)

    timeout = cfg.get('timeout')
    if timeout:
        context = LambdaContext(cfg.get('function_name'),timeout)
    else:
        context = LambdaContext(cfg.get('function_name'))

    start = time.time()
    results = fn(event, context)
    end = time.time()

    print('{0}'.format(results))
    if verbose:
        print('\nexecution time: {:.8f}s\nfunction execution '
              'timeout: {:2}s'.format(end - start, cfg.get('timeout', 15)))