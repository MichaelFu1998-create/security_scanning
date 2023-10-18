def run_as_root(command, *args, **kwargs):
    """
    Run a remote command as the root user.

    When connecting as root to the remote system, this will use Fabric's
    ``run`` function. In other cases, it will use ``sudo``.
    """
    from burlap.common import run_or_dryrun, sudo_or_dryrun
    if env.user == 'root':
        func = run_or_dryrun
    else:
        func = sudo_or_dryrun
    return func(command, *args, **kwargs)