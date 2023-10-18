def has_env_vars(*env_vars):
    """Raises `InvalidEnvironmentError` when one isnt set"""
    for env_var in env_vars:
        if not os.environ.get(env_var):
            msg = (
                'Must set {} environment variable. View docs for setting up environment at {}'
            ).format(env_var, temple.constants.TEMPLE_DOCS_URL)
            raise temple.exceptions.InvalidEnvironmentError(msg)