def is_installed(pkg_name):
    """
    Check if an RPM package is installed.
    """
    manager = MANAGER
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run("rpm --query %(pkg_name)s" % locals())
        if res.succeeded:
            return True
        return False