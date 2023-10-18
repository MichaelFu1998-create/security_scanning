def get_conf_filename():
    """
    The configuration file either lives in ~/.peri.json or is specified on the
    command line via the environment variables PERI_CONF_FILE
    """
    default = os.path.join(os.path.expanduser("~"), ".peri.json")
    return os.environ.get('PERI_CONF_FILE', default)