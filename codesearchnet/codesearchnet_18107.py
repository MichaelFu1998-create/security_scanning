def load_conf():
    """
    Load the configuration with the priority:
        1. environment variables
        2. configuration file
        3. defaults here (default_conf)
    """
    try:
        conf = copy.copy(default_conf)
        conf.update(json.load(open(get_conf_filename())))
        conf.update(read_environment())
        return conf
    except IOError as e:
        create_default_conf()
        return load_conf()