def iso_name_slugify(name):
    """Slugify a name in the ISO-9660 way.

    Example:
        >>> slugify('épatant')
        "_patant"
    """
    name = name.encode('ascii', 'replace').replace(b'?', b'_')
    return name.decode('ascii')