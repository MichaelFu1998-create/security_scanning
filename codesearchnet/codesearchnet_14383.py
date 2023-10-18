def read_temple_config():
    """Reads the temple YAML configuration file in the repository"""
    with open(temple.constants.TEMPLE_CONFIG_FILE) as temple_config_file:
        return yaml.load(temple_config_file, Loader=yaml.SafeLoader)