def distrib_family():
    """
    Get the distribution family.

    Returns one of ``debian``, ``redhat``, ``arch``, ``gentoo``,
    ``sun``, ``other``.
    """
    distrib = (distrib_id() or '').lower()
    if distrib in ['debian', 'ubuntu', 'linuxmint', 'elementary os']:
        return DEBIAN
    elif distrib in ['redhat', 'rhel', 'centos', 'sles', 'fedora']:
        return REDHAT
    elif distrib in ['sunos']:
        return SUN
    elif distrib in ['gentoo']:
        return GENTOO
    elif distrib in ['arch', 'manjarolinux']:
        return ARCH
    return 'other'