def lines_hash(lines):
    """
    Creates a unique binary id for the given lines
    Args:
        lines (list<str>): List of strings that should be collectively hashed
    Returns:
        bytearray: Binary hash
    """
    x = xxh32()
    for i in lines:
        x.update(i.encode())
    return x.digest()