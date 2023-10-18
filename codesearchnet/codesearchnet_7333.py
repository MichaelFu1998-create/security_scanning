def _load_ssh_auth_post_yosemite(mac_username):
    """Starting with Yosemite, launchd was rearchitected and now only one
    launchd process runs for all users. This allows us to much more easily
    impersonate a user through launchd and extract the environment
    variables from their running processes."""
    user_id = subprocess.check_output(['id', '-u', mac_username])
    ssh_auth_sock = subprocess.check_output(['launchctl', 'asuser', user_id, 'launchctl', 'getenv', 'SSH_AUTH_SOCK']).rstrip()
    _set_ssh_auth_sock(ssh_auth_sock)