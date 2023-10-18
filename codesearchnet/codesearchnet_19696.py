def is_oct(ip):
    """Return true if the IP address is in octal notation."""
    try:
        dec = int(str(ip), 8)
    except (TypeError, ValueError):
        return False
    if dec > 0o37777777777 or dec < 0:
        return False
    return True