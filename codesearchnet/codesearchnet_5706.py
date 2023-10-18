def _in_gce_environment():
    """Detect if the code is running in the Compute Engine environment.

    Returns:
        True if running in the GCE environment, False otherwise.
    """
    if SETTINGS.env_name is not None:
        return SETTINGS.env_name == 'GCE_PRODUCTION'

    if NO_GCE_CHECK != 'True' and _detect_gce_environment():
        SETTINGS.env_name = 'GCE_PRODUCTION'
        return True
    return False