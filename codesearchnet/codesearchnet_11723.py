def install(packages, update=False, options=None, version=None):
    """
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~burlap.deb.update_index`.

    Extra *options* may be passed to ``apt-get`` if necessary.

    Example::

        import burlap

        # Update index, then install a single package
        burlap.deb.install('build-essential', update=True)

        # Install multiple packages
        burlap.deb.install([
            'python-dev',
            'libxml2-dev',
        ])

        # Install a specific version
        burlap.deb.install('emacs', version='23.3+1-1ubuntu9')

    """
    manager = MANAGER
    if update:
        update_index()
    if options is None:
        options = []
    if version is None:
        version = ''
    if version and not isinstance(packages, list):
        version = '=' + version
    if not isinstance(packages, six.string_types):
        packages = " ".join(packages)
    options.append("--quiet")
    options.append("--assume-yes")
    options = " ".join(options)
    cmd = '%(manager)s install %(options)s %(packages)s%(version)s' % locals()
    run_as_root(cmd, pty=False)