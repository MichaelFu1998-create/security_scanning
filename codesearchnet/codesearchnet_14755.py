def update_floatingip(context, id, content):
    """Update an existing floating IP.

    :param context: neutron api request context.
    :param id: id of the floating ip
    :param content: dictionary with keys indicating fields to update.
        valid keys are those that have a value of True for 'allow_put'
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.

    :returns: Dictionary containing details for the new floating IP.  If values
        are declared in the fields parameter, then only those keys will be
        present.
    """

    LOG.info('update_floatingip %s for tenant %s and body %s' %
             (id, context.tenant_id, content))

    if 'port_id' not in content:
        raise n_exc.BadRequest(resource='floating_ip',
                               msg='port_id is required.')

    requested_ports = []
    if content.get('port_id'):
        requested_ports = [{'port_id': content.get('port_id')}]
    flip = _update_flip(context, id, ip_types.FLOATING, requested_ports)
    return v._make_floating_ip_dict(flip)