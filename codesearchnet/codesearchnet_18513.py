def _create_default_config():
    """ Writes the full default configuration to the appropriate place.
    Raises:
        IOError  - on unsuccesful file write
    :return: None
    """
    config_path = _get_config_path()
    with open(config_path, 'w+') as f:
        yaml.dump(_default_config, f, default_flow_style=False)