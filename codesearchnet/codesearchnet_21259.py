def get_own_ip():
    """
        Gets the IP from the inet interfaces.
    """
    own_ip = None
    interfaces = psutil.net_if_addrs()
    for _, details in interfaces.items():
        for detail in details:
            if detail.family == socket.AF_INET:
                ip_address = ipaddress.ip_address(detail.address)
                if not (ip_address.is_link_local or ip_address.is_loopback):
                    own_ip = str(ip_address)
                    break
    return own_ip