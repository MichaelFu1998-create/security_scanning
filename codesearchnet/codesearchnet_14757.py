def get_floatingip(context, id, fields=None):
    """Retrieve a floating IP.

    :param context: neutron api request context.
    :param id: The UUID of the floating IP.
    :param fields: a list of strings that are valid keys in a
        floating IP dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.

    :returns: Dictionary containing details for the floating IP.  If values
        are declared in the fields parameter, then only those keys will be
        present.
    """
    LOG.info('get_floatingip %s for tenant %s' % (id, context.tenant_id))

    filters = {'address_type': ip_types.FLOATING, '_deallocated': False}

    floating_ip = db_api.floating_ip_find(context, id=id, scope=db_api.ONE,
                                          **filters)

    if not floating_ip:
        raise q_exc.FloatingIpNotFound(id=id)

    return v._make_floating_ip_dict(floating_ip)