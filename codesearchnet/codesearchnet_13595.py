def is_ipv6_available():
    """Check if IPv6 is available.

    :Return: `True` when an IPv6 socket can be created.
    """
    try:
        socket.socket(socket.AF_INET6).close()
    except (socket.error, AttributeError):
        return False
    return True