def get_scalingips(context, filters=None, fields=None, sorts=['id'],
                   limit=None, marker=None, page_reverse=False):
    """Retrieve a list of scaling ips.

    :param context: neutron api request context.
    :param filters: a dictionary with keys that are valid keys for
        a scaling ip as listed in the RESOURCE_ATTRIBUTE_MAP object
        in neutron/api/v2/attributes.py.  Values in this dictionary
        are an iterable containing values that will be used for an exact
        match comparison for that value.  Each result returned by this
        function will have matched one of the values for each key in
        filters.
    :param fields: a list of strings that are valid keys in a
        scaling IP dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.

    :returns: List of scaling IPs that are accessible to the tenant who
        submits the request (as indicated by the tenant id of the context)
        as well as any filters.
    """
    LOG.info('get_scalingips for tenant %s filters %s fields %s' %
             (context.tenant_id, filters, fields))
    scaling_ips = _get_ips_by_type(context, ip_types.SCALING,
                                   filters=filters, fields=fields)
    return [v._make_scaling_ip_dict(scip) for scip in scaling_ips]