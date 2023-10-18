def get_os_version():
    """
    Returns a named tuple describing the operating system on the remote host.
    """

    # TODO: remove once fabric stops using contextlib.nested.
    # https://github.com/fabric/fabric/issues/1364
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    common_os_version = get_rc('common_os_version')
    if common_os_version:
        return common_os_version
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr', 'warnings'):

            ret = _run_or_local('cat /etc/lsb-release')
            if ret.succeeded:
                return OS(
                    type=LINUX,
                    distro=UBUNTU,
                    release=re.findall(r'DISTRIB_RELEASE=([0-9\.]+)', ret)[0])

            ret = _run_or_local('cat /etc/debian_version')
            if ret.succeeded:
                return OS(
                    type=LINUX,
                    distro=DEBIAN,
                    release=re.findall(r'([0-9\.]+)', ret)[0])

            ret = _run_or_local('cat /etc/fedora-release')
            if ret.succeeded:
                return OS(
                    type=LINUX,
                    distro=FEDORA,
                    release=re.findall(r'release ([0-9]+)', ret)[0])

            raise Exception('Unable to determine OS version.')