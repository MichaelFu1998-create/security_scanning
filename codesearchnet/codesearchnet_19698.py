def _check_nm(nm, notation):
    """Function internally used to check if the given netmask
    is of the specified notation."""
    # Convert to decimal, and check if it's in the list of valid netmasks.
    _NM_CHECK_FUNCT = {
        NM_DOT: _dot_to_dec,
        NM_HEX: _hex_to_dec,
        NM_BIN: _bin_to_dec,
        NM_OCT: _oct_to_dec,
        NM_DEC: _dec_to_dec_long}
    try:
        dec = _NM_CHECK_FUNCT[notation](nm, check=True)
    except ValueError:
        return False
    if dec in _NETMASKS_VALUES:
        return True
    return False