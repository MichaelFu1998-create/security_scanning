def check_and_load_ssh_auth():
    """
    Will check the mac_username config value; if it is present, will load that user's
    SSH_AUTH_SOCK environment variable to the current environment.  This allows git clones
    to behave the same for the daemon as they do for the user
    """

    mac_username = get_config_value(constants.CONFIG_MAC_USERNAME_KEY)
    if not mac_username:
        logging.info("Can't setup ssh authorization; no mac_username specified")
        return
    if not _running_on_mac(): # give our Linux unit tests a way to not freak out
        logging.info("Skipping SSH load, we are not running on Mac")
        return

    if _mac_version_is_post_yosemite():
        _load_ssh_auth_post_yosemite(mac_username)
    else:
        _load_ssh_auth_pre_yosemite()