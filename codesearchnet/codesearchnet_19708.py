def _dec_to_dec_long(ip, check=True):
    """Decimal to decimal (long) conversion."""
    if check and not is_dec(ip):
        raise ValueError('_dec_to_dec: invalid IP: "%s"' % ip)
    return int(str(ip))