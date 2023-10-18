def is_ipv4_available():
    """Check if IPv4 is available.

    :Return: `True` when an IPv4 socket can be created.
    """
    try:
        socket.socket(socket.AF_INET).close()
    except socket.error:
        return False
    return True