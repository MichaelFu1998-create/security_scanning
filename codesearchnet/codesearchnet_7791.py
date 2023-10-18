def parse_config_file(parser, stdin_args):
    """Parse config file.

    Returns a list of additional args.
    """
    config_args = []

    # Temporary switch required args and save them to restore.
    required_args = []
    for action in parser._actions:
        if action.required:
            required_args.append(action)
            action.required = False

    parsed_args = parser.parse_args(stdin_args)

    # Restore required args.
    for action in required_args:
        action.required = True

    if not parsed_args.config_file:
        return config_args

    config = ConfigParser()
    if not config.read(parsed_args.config_file):
        sys.stderr.write('Config file "{0}" doesn\'t exists\n'.format(parsed_args.config_file))
        sys.exit(7)  # It isn't used anywhere.

    config_args = _convert_config_to_stdin(config, parser)
    return config_args