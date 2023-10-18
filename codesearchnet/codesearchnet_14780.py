def get_subnets(context, limit=None, page_reverse=False, sorts=['id'],
                marker=None, filters=None, fields=None):
    """Retrieve a list of subnets.

    The contents of the list depends on the identity of the user
    making the request (as indicated by the context) as well as any
    filters.
    : param context: neutron api request context
    : param filters: a dictionary with keys that are valid keys for
        a subnet as listed in the RESOURCE_ATTRIBUTE_MAP object
        in neutron/api/v2/attributes.py.  Values in this dictiontary
        are an iterable containing values that will be used for an exact
        match comparison for that value.  Each result returned by this
        function will have matched one of the values for each key in
        filters.
    : param fields: a list of strings that are valid keys in a
        subnet dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_subnets for tenant %s with filters %s fields %s" %
             (context.tenant_id, filters, fields))
    filters = filters or {}
    subnets = db_api.subnet_find(context, limit=limit,
                                 page_reverse=page_reverse, sorts=sorts,
                                 marker_obj=marker, join_dns=True,
                                 join_routes=True, join_pool=True, **filters)
    for subnet in subnets:
        cache = subnet.get("_allocation_pool_cache")
        if not cache:
            db_api.subnet_update_set_alloc_pool_cache(
                context, subnet, subnet.allocation_pools)
    return v._make_subnets_list(subnets, fields=fields)