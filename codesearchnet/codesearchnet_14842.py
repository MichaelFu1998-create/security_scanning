def delete_mac_address_range(context, id):
    """Delete a mac_address_range.

    : param context: neutron api request context
    : param id: UUID representing the mac_address_range to delete.
    """
    LOG.info("delete_mac_address_range %s for tenant %s" %
             (id, context.tenant_id))
    if not context.is_admin:
        raise n_exc.NotAuthorized()

    with context.session.begin():
        mar = db_api.mac_address_range_find(context, id=id, scope=db_api.ONE)
        if not mar:
            raise q_exc.MacAddressRangeNotFound(
                mac_address_range_id=id)
        _delete_mac_address_range(context, mar)