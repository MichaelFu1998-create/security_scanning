def _wildcard_to_dec(nm, check=False):
    """Wildcard bits to decimal conversion."""
    if check and not is_wildcard_nm(nm):
        raise ValueError('_wildcard_to_dec: invalid netmask: "%s"' % nm)
    return 0xFFFFFFFF - _dot_to_dec(nm, check=False)