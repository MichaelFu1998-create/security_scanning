def _is_notation(ip, notation, _isnm):
    """Internally used to check if an IP/netmask is in the given notation."""
    notation_orig = notation
    notation = _get_notation(notation)
    if notation not in _CHECK_FUNCT_KEYS:
        raise ValueError('_is_notation: unkown notation: "%s"' % notation_orig)
    return _CHECK_FUNCT[notation][_isnm](ip)