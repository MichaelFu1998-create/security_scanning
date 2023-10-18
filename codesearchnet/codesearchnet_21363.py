def get_interface_name():
    """
        Returns the interface name of the first not link_local and not loopback interface.
    """
    interface_name = ''
    interfaces = psutil.net_if_addrs()
    for name, details in interfaces.items():
        for detail in details:
            if detail.family == socket.AF_INET:
                ip_address = ipaddress.ip_address(detail.address)
                if not (ip_address.is_link_local or ip_address.is_loopback):
                    interface_name = name
                    break
    return interface_name