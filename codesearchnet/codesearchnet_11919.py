def distrib_id():
    """
    Get the OS distribution ID.

    Example::

        from burlap.system import distrib_id

        if distrib_id() != 'Debian':
            abort(u"Distribution is not supported")

    """

    with settings(hide('running', 'stdout')):
        kernel = (run('uname -s') or '').strip().lower()
        if kernel == LINUX:
            # lsb_release works on Ubuntu and Debian >= 6.0
            # but is not always included in other distros
            if is_file('/usr/bin/lsb_release'):
                id_ = run('lsb_release --id --short').strip().lower()
                if id in ['arch', 'archlinux']:  # old IDs used before lsb-release 1.4-14
                    id_ = ARCH
                return id_
            else:
                if is_file('/etc/debian_version'):
                    return DEBIAN
                elif is_file('/etc/fedora-release'):
                    return FEDORA
                elif is_file('/etc/arch-release'):
                    return ARCH
                elif is_file('/etc/redhat-release'):
                    release = run('cat /etc/redhat-release')
                    if release.startswith('Red Hat Enterprise Linux'):
                        return REDHAT
                    elif release.startswith('CentOS'):
                        return CENTOS
                    elif release.startswith('Scientific Linux'):
                        return SLES
                elif is_file('/etc/gentoo-release'):
                    return GENTOO
        elif kernel == SUNOS:
            return SUNOS