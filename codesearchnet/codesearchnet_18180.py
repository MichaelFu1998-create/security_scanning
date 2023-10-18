def get_number_of_app_ports(app):
    """
    Get the number of ports for the given app JSON. This roughly follows the
    logic in marathon-lb for finding app IPs/ports, although we are only
    interested in the quantity of ports an app should have and don't consider
    the specific IPs/ports of individual tasks:
    https://github.com/mesosphere/marathon-lb/blob/v1.10.3/utils.py#L393-L415

    :param app: The app JSON from the Marathon API.
    :return: The number of ports for the app.
    """
    mode = _get_networking_mode(app)
    ports_list = None
    if mode == 'host':
        ports_list = _get_port_definitions(app)
    elif mode == 'container/bridge':
        ports_list = _get_port_definitions(app)
        if ports_list is None:
            ports_list = _get_container_port_mappings(app)
    elif mode == 'container':
        ports_list = _get_ip_address_discovery_ports(app)
        # Marathon 1.5+: the ipAddress field is missing -> ports_list is None
        # Marathon <1.5: the ipAddress field can be present, but ports_list can
        # still be empty while the container port mapping is not :-/
        if not ports_list:
            ports_list = _get_container_port_mappings(app)
    else:
        raise RuntimeError(
            "Unknown Marathon networking mode '{}'".format(mode))

    return len(ports_list)