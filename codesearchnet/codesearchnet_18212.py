def parse_listen_addr(listen_addr):
    """
    Parse an address of the form [ipaddress]:port into a tcp or tcp6 Twisted
    endpoint description string for use with
    ``twisted.internet.endpoints.serverFromString``.
    """
    if ':' not in listen_addr:
        raise ValueError(
            "'%s' does not have the correct form for a listen address: "
            '[ipaddress]:port' % (listen_addr,))
    host, port = listen_addr.rsplit(':', 1)

    # Validate the host
    if host == '':
        protocol = 'tcp'
        interface = None
    else:
        if host.startswith('[') and host.endswith(']'):  # IPv6 wrapped in []
            host = host[1:-1]
        ip_address = ipaddress.ip_address(_to_unicode(host))
        protocol = 'tcp6' if ip_address.version == 6 else 'tcp'
        interface = str(ip_address)

    # Validate the port
    if not port.isdigit() or int(port) < 1 or int(port) > 65535:
        raise ValueError(
            "'%s' does not appear to be a valid port number" % (port,))

    args = [protocol, port]
    kwargs = {'interface': interface} if interface is not None else {}

    return _create_tx_endpoints_string(args, kwargs)