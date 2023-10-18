def ip2long(ip):
    """
    Wrapper function for IPv4 and IPv6 converters.

    :arg ip: IPv4 or IPv6 address
    """
    try:
        return int(binascii.hexlify(socket.inet_aton(ip)), 16)
    except socket.error:
        return int(binascii.hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)