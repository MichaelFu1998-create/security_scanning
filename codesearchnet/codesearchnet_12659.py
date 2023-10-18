def is_valid_ip(ip_address):
    """ Check Validity of an IP address """

    try:
        ip = ipaddress.ip_address(u'' + ip_address)
        return True
    except ValueError as e:
        return False