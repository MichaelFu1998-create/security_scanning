def validate_xml_name(name):
    """validates XML name"""
    if len(name) == 0:
        raise RuntimeError('empty XML name')

    if __INVALID_NAME_CHARS & set(name):
        raise RuntimeError('XML name contains invalid character')

    if name[0] in __INVALID_NAME_START_CHARS:
        raise RuntimeError('XML name starts with invalid character')