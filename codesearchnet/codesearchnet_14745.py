def get_port(context, id, fields=None):
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
    results = db_api.port_find(context, id=id, fields=fields,
                               scope=db_api.ONE)

    if not results:
        raise n_exc.PortNotFound(port_id=id)

    return v._make_port_dict(results)