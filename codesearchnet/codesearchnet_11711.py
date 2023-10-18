def groupuninstall(group, options=None):
    """
    Remove an existing software group.

    Extra *options* may be passed to ``yum`` if necessary.

    """
    manager = MANAGER
    if options is None:
        options = []
    elif isinstance(options, str):
        options = [options]
    options = " ".join(options)
    run_as_root('%(manager)s %(options)s groupremove "%(group)s"' % locals())