def read_config(filename, args):
    """
    Read and parse configuration file. By default, ``filename`` is relative
    path to current work directory.

    If no config file found, default ``CONFIG`` would be used.

    :param filename: Read config from given filename.
    :param args: Parsed command line arguments.
    """
    # Initial vars
    config = defaultdict(dict)
    splitter = operator.methodcaller('split', ' ')

    converters = {
        __script__: {
            'env': safe_path,
            'pre_requirements': splitter,
        },
        'pip': {
            'allow_external': splitter,
            'allow_unverified': splitter,
        }
    }
    default = copy.deepcopy(CONFIG)
    sections = set(iterkeys(default))

    # Append download-cache for old pip versions
    if int(getattr(pip, '__version__', '1.x').split('.')[0]) < 6:
        default['pip']['download_cache'] = safe_path(os.path.expanduser(
            os.path.join('~', '.{0}'.format(__script__), 'pip-cache')
        ))

    # Expand user and environ vars in config filename
    is_default = filename == DEFAULT_CONFIG
    filename = os.path.expandvars(os.path.expanduser(filename))

    # Read config if it exists on disk
    if not is_default and not os.path.isfile(filename):
        print_error('Config file does not exist at {0!r}'.format(filename))
        return None

    parser = ConfigParser()

    try:
        parser.read(filename)
    except ConfigParserError:
        print_error('Cannot parse config file at {0!r}'.format(filename))
        return None

    # Apply config for each possible section
    for section in sections:
        if not parser.has_section(section):
            continue

        items = parser.items(section)

        # Make auto convert here for integers and boolean values
        for key, value in items:
            try:
                value = int(value)
            except (TypeError, ValueError):
                try:
                    value = bool(strtobool(value))
                except ValueError:
                    pass

            if section in converters and key in converters[section]:
                value = converters[section][key](value)

            config[section][key] = value

    # Update config with default values if necessary
    for section, data in iteritems(default):
        if section not in config:
            config[section] = data
        else:
            for key, value in iteritems(data):
                config[section].setdefault(key, value)

    # Update bootstrap config from parsed args
    keys = set((
        'env', 'hook', 'install_dev_requirements', 'ignore_activated',
        'pre_requirements', 'quiet', 'recreate', 'requirements'
    ))

    for key in keys:
        value = getattr(args, key)
        config[__script__].setdefault(key, value)

        if key == 'pre_requirements' and not value:
            continue

        if value is not None:
            config[__script__][key] = value

    return config