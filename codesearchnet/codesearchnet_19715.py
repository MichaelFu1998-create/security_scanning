def convert_nm(nm, notation=IP_DOT, inotation=IP_UNKNOWN, check=True):
    """Convert a netmask to another notation."""
    return _convert(nm, notation, inotation, _check=check, _isnm=True)