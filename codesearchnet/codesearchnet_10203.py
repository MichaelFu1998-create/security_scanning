def get_credentials_from_file(filepath):
    """
    Extracts credentials from the yaml formatted credential filepath
    passed in. Uses the default profile if the CITRINATION_PROFILE env var
    is not set, otherwise looks for a profile with that name in the credentials file.

    :param filepath: The path of the credentials file
    """
    try:
        creds = load_file_as_yaml(filepath)
    except Exception:
        creds = {}

    profile_name = os.environ.get(citr_env_vars.CITRINATION_PROFILE)
    if profile_name is None or len(profile_name) == 0:
        profile_name = DEFAULT_CITRINATION_PROFILE
    api_key = None
    site = None
    try:
        profile = creds[profile_name]
        api_key = profile[CREDENTIALS_API_KEY_KEY]
        site = profile[CREDENTIALS_SITE_KEY]
    except KeyError:
        pass

    return (api_key, site)