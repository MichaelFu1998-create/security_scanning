def _dec_to_dot(ip):
    """Decimal to dotted decimal notation conversion."""
    first = int((ip >> 24) & 255)
    second = int((ip >> 16) & 255)
    third = int((ip >> 8) & 255)
    fourth = int(ip & 255)
    return '%d.%d.%d.%d' % (first, second, third, fourth)