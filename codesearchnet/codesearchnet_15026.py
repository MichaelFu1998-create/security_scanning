def get_pypi_auth(configfile='~/.pypirc'):
    """Read auth from pip config."""
    pypi_cfg = ConfigParser()
    if pypi_cfg.read(os.path.expanduser(configfile)):
        try:
            user = pypi_cfg.get('pypi', 'username')
            pwd = pypi_cfg.get('pypi', 'password')
            return user, pwd
        except ConfigError:
            notify.warning("No PyPI credentials in '{}',"
                           " will fall back to '~/.netrc'...".format(configfile))
    return None