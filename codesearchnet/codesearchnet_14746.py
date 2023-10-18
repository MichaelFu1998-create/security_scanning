def get_ports(context, limit=None, sorts=['id'], marker=None,
              page_reverse=False, filters=None, fields=None):
    """Retrieve a list of ports.

    The contents of the list depends on the identity of the user
    making the request (as indicated by the context) as well as any
    filters.
    : param context: neutron api request context
    : param filters: a dictionary with keys that are valid keys for
        a port as listed in the RESOURCE_ATTRIBUTE_MAP object
        in neutron/api/v2/attributes.py.  Values in this dictionary
        are an iterable containing values that will be used for an exact
        match comparison for that value.  Each result returned by this
        function will have matched one of the values for each key in
        filters.
    : param fields: a list of strings that are valid keys in a
        port dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_ports for tenant %s filters %s fields %s" %
             (context.tenant_id, filters, fields))
    if filters is None:
        filters = {}

    if "ip_address" in filters:
        if not context.is_admin:
            raise n_exc.NotAuthorized()
        ips = []
        try:
            ips = [netaddr.IPAddress(ip) for ip in filters.pop("ip_address")]
        except netaddr.AddrFormatError:
            raise n_exc.InvalidInput(
                error_message="Invalid format provided for ip_address")
        query = db_api.port_find_by_ip_address(context, ip_address=ips,
                                               scope=db_api.ALL, **filters)
        ports = []
        for ip in query:
            ports.extend(ip.ports)
    else:
        ports = db_api.port_find(context, limit, sorts, marker,
                                 fields=fields, join_security_groups=True,
                                 **filters)
    return v._make_ports_list(ports, fields)