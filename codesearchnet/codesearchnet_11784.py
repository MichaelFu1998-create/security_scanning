def get_packager():
    """
    Returns the packager detected on the remote system.
    """

    # TODO: remove once fabric stops using contextlib.nested.
    # https://github.com/fabric/fabric/issues/1364
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    common_packager = get_rc('common_packager')
    if common_packager:
        return common_packager
    #TODO:cache result by current env.host_string so we can handle multiple hosts with different OSes
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr', 'warnings'):
            ret = _run('cat /etc/fedora-release')
            if ret.succeeded:
                common_packager = YUM
            else:
                ret = _run('cat /etc/lsb-release')
                if ret.succeeded:
                    common_packager = APT
                else:
                    for pn in PACKAGERS:
                        ret = _run('which %s' % pn)
                        if ret.succeeded:
                            common_packager = pn
                            break
    if not common_packager:
        raise Exception('Unable to determine packager.')
    set_rc('common_packager', common_packager)
    return common_packager