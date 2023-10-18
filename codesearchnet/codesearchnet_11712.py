def repolist(status='', media=None):
    """
    Get the list of ``yum`` repositories.

    Returns enabled repositories by default. Extra *status* may be passed
    to list disabled repositories if necessary.

    Media and debug repositories are kept disabled, except if you pass *media*.

    ::

        import burlap

        # Install a package that may be included in disabled repositories
        burlap.rpm.install('vim', burlap.rpm.repolist('disabled'))

    """
    manager = MANAGER
    with settings(hide('running', 'stdout')):
        if media:
            repos = run_as_root("%(manager)s repolist %(status)s | sed '$d' | sed -n '/repo id/,$p'" % locals())
        else:
            repos = run_as_root("%(manager)s repolist %(status)s | sed '/Media\\|Debug/d' | sed '$d' | sed -n '/repo id/,$p'" % locals())
        return [line.split(' ')[0] for line in repos.splitlines()[1:]]