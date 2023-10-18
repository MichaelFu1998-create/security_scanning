def update_scalingip(context, id, content):
    """Update an existing scaling IP.

    :param context: neutron api request context.
    :param id: id of the scaling ip
    :param content: dictionary with keys indicating fields to update.
        valid keys are those that have a value of True for 'allow_put'
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.

    :returns: Dictionary containing details for the new scaling IP.  If values
        are declared in the fields parameter, then only those keys will be
        present.
    """
    LOG.info('update_scalingip %s for tenant %s and body %s' %
             (id, context.tenant_id, content))
    requested_ports = content.get('ports', [])
    flip = _update_flip(context, id, ip_types.SCALING, requested_ports)
    return v._make_scaling_ip_dict(flip)