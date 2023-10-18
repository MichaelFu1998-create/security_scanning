def is_local_ip(ip_address):
    """ Check if IP is local """

    try:
        ip = ipaddress.ip_address(u'' + ip_address)
        return ip.is_loopback
    except ValueError as e:
        return None