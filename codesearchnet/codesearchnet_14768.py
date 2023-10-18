def get_port_for_ip_address(context, ip_id, id, fields=None):
    """Retrieve a port.

    : param context: neutron api request context
    : param id: UUID representing the port to fetch.
    : param fields: a list of strings that are valid keys in a
        port dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_port %s for tenant %s fields %s" %
             (id, context.tenant_id, fields))
    addr = db_api.ip_address_find(context, id=ip_id, scope=db_api.ONE)
    if not addr:
        raise q_exc.IpAddressNotFound(addr_id=ip_id)

    filters = {'ip_address_id': [ip_id]}
    results = db_api.port_find(context, id=id, fields=fields,
                               scope=db_api.ONE, **filters)

    if not results:
        raise n_exc.PortNotFound(port_id=id)

    return v._make_port_for_ip_dict(addr, results)