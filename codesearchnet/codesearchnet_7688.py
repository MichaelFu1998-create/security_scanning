def load_config():
    """Load a keyring using the config file in the config root."""

    filename = 'keyringrc.cfg'

    keyring_cfg = os.path.join(platform.config_root(), filename)

    if not os.path.exists(keyring_cfg):
        return

    config = configparser.RawConfigParser()
    config.read(keyring_cfg)
    _load_keyring_path(config)

    # load the keyring class name, and then load this keyring
    try:
        if config.has_section("backend"):
            keyring_name = config.get("backend", "default-keyring").strip()
        else:
            raise configparser.NoOptionError('backend', 'default-keyring')

    except (configparser.NoOptionError, ImportError):
        logger = logging.getLogger('keyring')
        logger.warning("Keyring config file contains incorrect values.\n"
                       + "Config file: %s" % keyring_cfg)
        return

    return load_keyring(keyring_name)