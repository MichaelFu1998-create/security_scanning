def get_floatingips_count(context, filters=None):
    """Return the number of floating IPs.

    :param context: neutron api request context
    :param filters: a dictionary with keys that are valid keys for
        a floating IP as listed in the RESOURCE_ATTRIBUTE_MAP object
        in neutron/api/v2/attributes.py.  Values in this dictionary
        are an iterable containing values that will be used for an exact
        match comparison for that value.  Each result returned by this
        function will have matched one of the values for each key in
        filters.

    :returns: The number of floating IPs that are accessible to the tenant who
        submits the request (as indicated by the tenant id of the context)
        as well as any filters.

    NOTE: this method is optional, as it was not part of the originally
          defined plugin API.
    """
    LOG.info('get_floatingips_count for tenant %s filters %s' %
             (context.tenant_id, filters))

    if filters is None:
        filters = {}

    filters['_deallocated'] = False
    filters['address_type'] = ip_types.FLOATING
    count = db_api.ip_address_count_all(context, filters)

    LOG.info('Found %s floating ips for tenant %s' % (count,
                                                      context.tenant_id))
    return count