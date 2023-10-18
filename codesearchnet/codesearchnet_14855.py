def get_networks(context, limit=None, sorts=['id'], marker=None,
                 page_reverse=False, filters=None, fields=None):
    """Retrieve a list of networks.

    The contents of the list depends on the identity of the user
    making the request (as indicated by the context) as well as any
    filters.
    : param context: neutron api request context
    : param filters: a dictionary with keys that are valid keys for
        a network as listed in the RESOURCE_ATTRIBUTE_MAP object
        in neutron/api/v2/attributes.py.  Values in this dictiontary
        are an iterable containing values that will be used for an exact
        match comparison for that value.  Each result returned by this
        function will have matched one of the values for each key in
        filters.
    : param fields: a list of strings that are valid keys in a
        network dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_networks for tenant %s with filters %s, fields %s" %
             (context.tenant_id, filters, fields))
    filters = filters or {}
    nets = db_api.network_find(context, limit, sorts, marker, page_reverse,
                               join_subnets=True, **filters) or []
    nets = [v._make_network_dict(net, fields=fields) for net in nets]
    return nets