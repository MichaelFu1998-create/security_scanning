def get_mac_address_range(context, id, fields=None):
    """Retrieve a mac_address_range.

    : param context: neutron api request context
    : param id: UUID representing the network to fetch.
    : param fields: a list of strings that are valid keys in a
        network dictionary as listed in the RESOURCE_ATTRIBUTE_MAP
        object in neutron/api/v2/attributes.py. Only these fields
        will be returned.
    """
    LOG.info("get_mac_address_range %s for tenant %s fields %s" %
             (id, context.tenant_id, fields))

    if not context.is_admin:
        raise n_exc.NotAuthorized()

    mac_address_range = db_api.mac_address_range_find(
        context, id=id, scope=db_api.ONE)

    if not mac_address_range:
        raise q_exc.MacAddressRangeNotFound(
            mac_address_range_id=id)
    return v._make_mac_range_dict(mac_address_range)