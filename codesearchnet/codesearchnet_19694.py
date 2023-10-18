def is_dot(ip):
    """Return true if the IP address is in dotted decimal notation."""
    octets = str(ip).split('.')
    if len(octets) != 4:
        return False
    for i in octets:
        try:
            val = int(i)
        except ValueError:
            return False
        if val > 255 or val < 0:
            return False
    return True