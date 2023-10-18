def _dot_to_dec(ip, check=True):
    """Dotted decimal notation to decimal conversion."""
    if check and not is_dot(ip):
        raise ValueError('_dot_to_dec: invalid IP: "%s"' % ip)
    octets = str(ip).split('.')
    dec = 0
    dec |= int(octets[0]) << 24
    dec |= int(octets[1]) << 16
    dec |= int(octets[2]) << 8
    dec |= int(octets[3])
    return dec