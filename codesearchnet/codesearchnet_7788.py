def supported_versions(django, cms):
    """
    Convert numeric and literal version information to numeric format
    """
    cms_version = None
    django_version = None

    try:
        cms_version = Decimal(cms)
    except (ValueError, InvalidOperation):
        try:
            cms_version = CMS_VERSION_MATRIX[str(cms)]
        except KeyError:
            pass

    try:
        django_version = Decimal(django)
    except (ValueError, InvalidOperation):
        try:
            django_version = DJANGO_VERSION_MATRIX[str(django)]
        except KeyError:  # pragma: no cover
            pass

    try:
        if (
                cms_version and django_version and
                not (LooseVersion(VERSION_MATRIX[compat.unicode(cms_version)][0]) <=
                     LooseVersion(compat.unicode(django_version)) <=
                     LooseVersion(VERSION_MATRIX[compat.unicode(cms_version)][1]))
        ):
            raise RuntimeError(
                'Django and django CMS versions doesn\'t match: '
                'Django {0} is not supported by django CMS {1}'.format(django_version, cms_version)
            )
    except KeyError:
        raise RuntimeError(
            'Django and django CMS versions doesn\'t match: '
            'Django {0} is not supported by django CMS {1}'.format(django_version, cms_version)
        )
    return (
        compat.unicode(django_version) if django_version else django_version,
        compat.unicode(cms_version) if cms_version else cms_version
    )