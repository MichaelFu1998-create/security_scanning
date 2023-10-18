def uninstall(packages, options=None):
    """
    Remove one or more packages.

    Extra *options* may be passed to ``yum`` if necessary.

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, six.string_types):
        options = [options]
    if not isinstance(packages, six.string_types):
        packages = " ".join(packages)
    options = " ".join(options)
    run_as_root('%(manager)s %(options)s remove %(packages)s' % locals())