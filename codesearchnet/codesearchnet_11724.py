def uninstall(packages, purge=False, options=None):
    """
    Remove one or more packages.

    If *purge* is ``True``, the package configuration files will be
    removed from the system.

    Extra *options* may be passed to ``apt-get`` if necessary.
    """
    manager = MANAGER
    command = "purge" if purge else "remove"
    if options is None:
        options = []
    if not isinstance(packages, six.string_types):
        packages = " ".join(packages)
    options.append("--assume-yes")
    options = " ".join(options)
    cmd = '%(manager)s %(command)s %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)