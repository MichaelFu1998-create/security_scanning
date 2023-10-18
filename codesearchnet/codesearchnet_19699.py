def is_bits_nm(nm):
    """Return true if the netmask is in bits notatation."""
    try:
        bits = int(str(nm))
    except ValueError:
        return False
    if bits > 32 or bits < 0:
        return False
    return True