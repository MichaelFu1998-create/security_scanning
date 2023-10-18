def install(packages, repos=None, yes=None, options=None):
    """
    Install one or more RPM packages.

    Extra *repos* may be passed to ``yum`` to enable extra repositories at install time.

    Extra *yes* may be passed to ``yum`` to validate license if necessary.

    Extra *options* may be passed to ``yum`` if necessary
    (e.g. ``['--nogpgcheck', '--exclude=package']``).

    ::

        import burlap

        # Install a single package, in an alternative install root
        burlap.rpm.install('emacs', options='--installroot=/my/new/location')

        # Install multiple packages silently
        burlap.rpm.install([
            'unzip',
            'nano'
        ], '--quiet')

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, six.string_types):
        options = [options]
    if not isinstance(packages, six.string_types):
        packages = " ".join(packages)
    if repos:
        for repo in repos:
            options.append('--enablerepo=%(repo)s' % locals())
    options = " ".join(options)
    if isinstance(yes, str):
        run_as_root('yes %(yes)s | %(manager)s %(options)s install %(packages)s' % locals())
    else:
        run_as_root('%(manager)s %(options)s install %(packages)s' % locals())