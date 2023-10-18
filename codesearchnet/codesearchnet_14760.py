def create_scalingip(context, content):
    """Allocate or reallocate a scaling IP.

    :param context: neutron api request context.
    :param content: dictionary describing the scaling ip, with keys
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.  All keys will be populated.

    :returns: Dictionary containing details for the new scaling IP.  If values
        are declared in the fields parameter, then only those keys will be
        present.
    """
    LOG.info('create_scalingip for tenant %s and body %s',
             context.tenant_id, content)
    network_id = content.get('scaling_network_id')
    ip_address = content.get('scaling_ip_address')
    requested_ports = content.get('ports', [])

    network = _get_network(context, network_id)
    port_fixed_ips = {}
    for req_port in requested_ports:
        port = _get_port(context, req_port['port_id'])
        fixed_ip = _get_fixed_ip(context, req_port.get('fixed_ip_address'),
                                 port)
        port_fixed_ips[port.id] = {"port": port, "fixed_ip": fixed_ip}
    scip = _allocate_ip(context, network, None, ip_address, ip_types.SCALING)
    _create_flip(context, scip, port_fixed_ips)
    return v._make_scaling_ip_dict(scip)