def supported_locales():
    """
    Gets the list of supported locales.

    Each locale is returned as a ``(locale, charset)`` tuple.
    """
    family = distrib_family()
    if family == 'debian':
        return _parse_locales('/usr/share/i18n/SUPPORTED')
    elif family == 'arch':
        return _parse_locales('/etc/locale.gen')
    elif family == 'redhat':
        return _supported_locales_redhat()
    else:
        raise UnsupportedFamily(supported=['debian', 'arch', 'redhat'])