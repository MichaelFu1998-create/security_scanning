def _load_ssh_auth_pre_yosemite():
    """For OS X versions before Yosemite, many launchd processes run simultaneously under
    different users and different permission models. The simpler `asuser` trick we use
    in Yosemite doesn't work, since it gets routed to the wrong launchd. We instead need
    to find the running ssh-agent process and use its PID to navigate ourselves
    to the correct launchd."""
    for process in psutil.process_iter():
        if process.name() == 'ssh-agent':
            ssh_auth_sock = subprocess.check_output(['launchctl', 'bsexec', str(process.pid), 'launchctl', 'getenv', 'SSH_AUTH_SOCK']).rstrip()
            if ssh_auth_sock:
                _set_ssh_auth_sock(ssh_auth_sock)
                break
    else:
        daemon_warnings.warn('ssh', 'No running ssh-agent found linked to SSH_AUTH_SOCK')