def get_subnet(context, id, fields=None):
    """Retrieve a subnet.

    : param context: neutron api request context
    : param id: UUID representing the subnet to fetch.
    : param fields: a list of strings that are valid keys in a
        subnet dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_subnet %s for tenant %s with fields %s" %
             (id, context.tenant_id, fields))
    subnet = db_api.subnet_find(context=context, limit=None,
                                page_reverse=False, sorts=['id'],
                                marker_obj=None, fields=None, id=id,
                                join_dns=True, join_routes=True,
                                scope=db_api.ONE)
    if not subnet:
        raise n_exc.SubnetNotFound(subnet_id=id)

    cache = subnet.get("_allocation_pool_cache")
    if not cache:
        new_cache = subnet.allocation_pools
        db_api.subnet_update_set_alloc_pool_cache(context, subnet, new_cache)
    return v._make_subnet_dict(subnet)