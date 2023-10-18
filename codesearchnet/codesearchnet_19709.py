def _bits_to_dec(nm, check=True):
    """Bits to decimal conversion."""
    if check and not is_bits_nm(nm):
        raise ValueError('_bits_to_dec: invalid netmask: "%s"' % nm)
    bits = int(str(nm))
    return VALID_NETMASKS[bits]