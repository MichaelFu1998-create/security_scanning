def get_scalingip(context, id, fields=None):
    """Retrieve a scaling IP.

    :param context: neutron api request context.
    :param id: The UUID of the scaling IP.
    :param fields: a list of strings that are valid keys in a
        scaling IP dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.

    :returns: Dictionary containing details for the scaling IP.  If values
        are declared in the fields parameter, then only those keys will be
        present.
    """
    LOG.info('get_scalingip %s for tenant %s' % (id, context.tenant_id))
    filters = {'address_type': ip_types.SCALING, '_deallocated': False}
    scaling_ip = db_api.floating_ip_find(context, id=id, scope=db_api.ONE,
                                         **filters)
    if not scaling_ip:
        raise q_exc.ScalingIpNotFound(id=id)
    return v._make_scaling_ip_dict(scaling_ip)