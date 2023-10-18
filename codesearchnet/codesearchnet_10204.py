def get_preferred_credentials(api_key, site, cred_file=DEFAULT_CITRINATION_CREDENTIALS_FILE):
    """
    Given an API key, a site url and a credentials file path, runs through a prioritized list of credential sources to find credentials.

    Specifically, this method ranks credential priority as follows:
        1. Those passed in as the first two parameters to this method
        2. Those found in the environment as variables
        3. Those found in the credentials file at the profile specified
           by the profile environment variable
        4. Those found in the default stanza in the credentials file

    :param api_key: A Citrination API Key or None
    :param site: A Citrination site URL or None
    :param cred_file: The path to a credentials file
    """
    profile_api_key, profile_site = get_credentials_from_file(cred_file)
    if api_key is None:
        api_key =  os.environ.get(citr_env_vars.CITRINATION_API_KEY)
    if api_key is None or len(api_key) == 0:
        api_key = profile_api_key

    if site is None:
        site = os.environ.get(citr_env_vars.CITRINATION_SITE)
    if site is None or len(site) == 0:
        site = profile_site
    if site is None:
        site = "https://citrination.com"

    return api_key, site