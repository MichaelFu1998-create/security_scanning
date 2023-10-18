def get_network(context, id, fields=None):
    """Retrieve a network.

    : param context: neutron api request context
    : param id: UUID representing the network to fetch.
    : param fields: a list of strings that are valid keys in a
        network dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_network %s for tenant %s fields %s" %
             (id, context.tenant_id, fields))

    network = db_api.network_find(context=context, limit=None, sorts=['id'],
                                  marker=None, page_reverse=False,
                                  id=id, join_subnets=True, scope=db_api.ONE)
    if not network:
        raise n_exc.NetworkNotFound(net_id=id)
    return v._make_network_dict(network, fields=fields)