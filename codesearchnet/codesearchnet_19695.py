def is_bin(ip):
    """Return true if the IP address is in binary notation."""
    try:
        ip = str(ip)
        if len(ip) != 32:
            return False
        dec = int(ip, 2)
    except (TypeError, ValueError):
        return False
    if dec > 4294967295 or dec < 0:
        return False
    return True