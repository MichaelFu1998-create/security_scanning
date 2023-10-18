def _hex_to_dec(ip, check=True):
    """Hexadecimal to decimal conversion."""
    if check and not is_hex(ip):
        raise ValueError('_hex_to_dec: invalid IP: "%s"' % ip)
    if isinstance(ip, int):
        ip = hex(ip)
    return int(str(ip), 16)