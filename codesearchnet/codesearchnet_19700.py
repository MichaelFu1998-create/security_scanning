def is_wildcard_nm(nm):
    """Return true if the netmask is in wildcard bits notatation."""
    try:
        dec = 0xFFFFFFFF - _dot_to_dec(nm, check=True)
    except ValueError:
        return False
    if dec in _NETMASKS_VALUES:
        return True
    return False