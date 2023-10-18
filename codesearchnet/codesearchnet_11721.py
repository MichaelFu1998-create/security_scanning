def upgrade(safe=True):
    """
    Upgrade all packages.
    """
    manager = MANAGER
    if safe:
        cmd = 'upgrade'
    else:
        cmd = 'dist-upgrade'
    run_as_root("%(manager)s --assume-yes %(cmd)s" % locals(), pty=False)