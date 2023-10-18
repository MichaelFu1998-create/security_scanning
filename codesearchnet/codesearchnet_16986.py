def parse_configfile(configfile):
    """
    Read settings from file
    :param configfile:
    """
    with open(configfile) as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            logging.fatal("Could not load default config file: %s", e)
            exit(-1)