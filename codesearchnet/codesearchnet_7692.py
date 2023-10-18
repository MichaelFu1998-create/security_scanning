def _config_root_Linux():
    """
    Use freedesktop.org Base Dir Specfication to determine config
    location.
    """
    _check_old_config_root()
    fallback = os.path.expanduser('~/.local/share')
    key = 'XDG_CONFIG_HOME'
    root = os.environ.get(key, None) or fallback
    return os.path.join(root, 'python_keyring')