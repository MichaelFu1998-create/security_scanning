def groupinstall(group, options=None):
    """
    Install a group of packages.

    You can use ``yum grouplist`` to get the list of groups.

    Extra *options* may be passed to ``yum`` if necessary like
    (e.g. ``['--nogpgcheck', '--exclude=package']``).

    ::

        import burlap

        # Install development packages
        burlap.rpm.groupinstall('Development tools')

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    options = " ".join(options)
    run_as_root('%(manager)s %(options)s groupinstall "%(group)s"' % locals(), pty=False)