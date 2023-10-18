def _validate_ip_address(family, address):
    """Check if `address` is valid IP address and return it, in a normalized
    form.

    :Parameters:
        - `family`: ``socket.AF_INET`` or ``socket.AF_INET6``
        - `address`: the IP address to validate
    """
    try:
        info = socket.getaddrinfo(address, 0, family, socket.SOCK_STREAM, 0,
                                                        socket.AI_NUMERICHOST)
    except socket.gaierror, err:
        logger.debug("gaierror: {0} for {1!r}".format(err, address))
        raise ValueError("Bad IP address")

    if not info:
        logger.debug("getaddrinfo result empty")
        raise ValueError("Bad IP address")
    addr = info[0][4]
    logger.debug(" got address: {0!r}".format(addr))

    try:
        return socket.getnameinfo(addr, socket.NI_NUMERICHOST)[0]
    except socket.gaierror, err:
        logger.debug("gaierror: {0} for {1!r}".format(err, addr))
        raise ValueError("Bad IP address")