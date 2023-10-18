def update(kernel=False):
    """
    Upgrade all packages, skip obsoletes if ``obsoletes=0`` in ``yum.conf``.

    Exclude *kernel* upgrades by default.
    """
    manager = MANAGER
    cmds = {'yum -y --color=never': {False: '--exclude=kernel* update', True: 'update'}}
    cmd = cmds[manager][kernel]
    run_as_root("%(manager)s %(cmd)s" % locals())