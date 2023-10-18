def distrib_release():
    """
    Get the release number of the distribution.

    Example::

        from burlap.system import distrib_id, distrib_release

        if distrib_id() == 'CentOS' and distrib_release() == '6.1':
            print(u"CentOS 6.2 has been released. Please upgrade.")

    """
    with settings(hide('running', 'stdout')):
        kernel = (run('uname -s') or '').strip().lower()
        if kernel == LINUX:
            return run('lsb_release -r --short')

        elif kernel == SUNOS:
            return run('uname -v')