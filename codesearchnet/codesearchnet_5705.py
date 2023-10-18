def _in_gae_environment():
    """Detects if the code is running in the App Engine environment.

    Returns:
        True if running in the GAE environment, False otherwise.
    """
    if SETTINGS.env_name is not None:
        return SETTINGS.env_name in ('GAE_PRODUCTION', 'GAE_LOCAL')

    try:
        import google.appengine  # noqa: unused import
    except ImportError:
        pass
    else:
        server_software = os.environ.get(_SERVER_SOFTWARE, '')
        if server_software.startswith('Google App Engine/'):
            SETTINGS.env_name = 'GAE_PRODUCTION'
            return True
        elif server_software.startswith('Development/'):
            SETTINGS.env_name = 'GAE_LOCAL'
            return True

    return False