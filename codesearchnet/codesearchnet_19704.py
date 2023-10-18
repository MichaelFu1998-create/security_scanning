def _oct_to_dec(ip, check=True):
    """Octal to decimal conversion."""
    if check and not is_oct(ip):
        raise ValueError('_oct_to_dec: invalid IP: "%s"' % ip)
    if isinstance(ip, int):
        ip = oct(ip)
    return int(str(ip), 8)