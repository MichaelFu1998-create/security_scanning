def create_floatingip(context, content):
    """Allocate or reallocate a floating IP.

    :param context: neutron api request context.
    :param content: dictionary describing the floating ip, with keys
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.  All keys will be populated.

    :returns: Dictionary containing details for the new floating IP.  If values
        are declared in the fields parameter, then only those keys will be
        present.
    """
    LOG.info('create_floatingip %s for tenant %s and body %s' %
             (id, context.tenant_id, content))
    network_id = content.get('floating_network_id')
    # TODO(blogan): Since the extension logic will reject any requests without
    # floating_network_id, is this still needed?
    if not network_id:
        raise n_exc.BadRequest(resource='floating_ip',
                               msg='floating_network_id is required.')
    fixed_ip_address = content.get('fixed_ip_address')
    ip_address = content.get('floating_ip_address')
    port_id = content.get('port_id')
    port = None
    port_fixed_ip = {}

    network = _get_network(context, network_id)
    if port_id:
        port = _get_port(context, port_id)
        fixed_ip = _get_fixed_ip(context, fixed_ip_address, port)
        port_fixed_ip = {port.id: {'port': port, 'fixed_ip': fixed_ip}}
    flip = _allocate_ip(context, network, port, ip_address, ip_types.FLOATING)
    _create_flip(context, flip, port_fixed_ip)
    return v._make_floating_ip_dict(flip, port_id)