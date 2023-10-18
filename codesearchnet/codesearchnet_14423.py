def _parse_and_output(filename, args):
    """
    Parse `filename` appropriately and then output calls according to the
    `args` specified.

    :param filename: A file or directory
    :param args: Command arguments
    :type filename: str

    """
    relpath = os.path.dirname(filename)
    if os.path.isfile(filename):
        calls = _parse_file(filename, relpath)
    elif os.path.isdir(filename):
        calls = _parse_dir(filename, relpath)
    else:
        # XXX(shakefu): This is an error of some sort, maybe symlinks?
        # Probably need some thorough testing
        _error("Could not determine file type: %r", filename)

    if not calls:
        # XXX(shakefu): Probably want to change this to not be an error and
        # just be a normal fail (e.g. command runs, no output).
        _error("No pyconfig calls.")

    if args.load_configs:
        # We want to iterate over the configs and add any keys which haven't
        # already been found
        keys = set()
        for call in calls:
            keys.add(call.key)

        # Iterate the loaded keys and make _PyconfigCall instances
        conf = pyconfig.Config()
        for key, value in conf.settings.items():
            if key in keys:
                continue
            calls.append(_PyconfigCall('set', key, value, [None]*4))

    _output(calls, args)