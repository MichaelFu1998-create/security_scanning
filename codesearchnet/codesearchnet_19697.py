def is_dec(ip):
    """Return true if the IP address is in decimal notation."""
    try:
        dec = int(str(ip))
    except ValueError:
        return False
    if dec > 4294967295 or dec < 0:
        return False
    return True