def load_config():
    """
    Load settings from default config and optionally
    overwrite with config file and commandline parameters
    (in that order).
    """
    # We start with the default config
    config = flatten(default_config.DEFAULT_CONFIG)

    # Read commandline arguments
    cli_config = flatten(parse_args())

    if "configfile" in cli_config:
        logging.info("Reading config file {}".format(cli_config['configfile']))
        configfile = parse_configfile(cli_config['configfile'])
        config = overwrite_config(config, configfile)

    # Parameters from commandline take precedence over all others
    config = overwrite_config(config, cli_config)

    # Set verbosity level
    if 'verbose' in config:
        if config['verbose'] == 1:
            logging.getLogger().setLevel(logging.INFO)
        elif config['verbose'] > 1:
            logging.getLogger().setLevel(logging.DEBUG)

    return ObjectView(config)