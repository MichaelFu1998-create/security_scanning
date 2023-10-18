def _bin_to_dec(ip, check=True):
    """Binary to decimal conversion."""
    if check and not is_bin(ip):
        raise ValueError('_bin_to_dec: invalid IP: "%s"' % ip)
    if isinstance(ip, int):
        ip = str(ip)
    return int(str(ip), 2)