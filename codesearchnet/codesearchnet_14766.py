def delete_ip_address(context, id):
    """Delete an ip address.

    : param context: neutron api request context
    : param id: UUID representing the ip address to delete.
    """
    LOG.info("delete_ip_address %s for tenant %s" % (id, context.tenant_id))
    with context.session.begin():
        ip_address = db_api.ip_address_find(
            context, id=id, scope=db_api.ONE)
        if not ip_address or ip_address.deallocated:
            raise q_exc.IpAddressNotFound(addr_id=id)

        iptype = ip_address.address_type
        if iptype == ip_types.FIXED and not CONF.QUARK.ipaddr_allow_fixed_ip:
            raise n_exc.BadRequest(
                resource="ip_addresses",
                msg="Fixed ips cannot be updated using this interface.")

        if ip_address.has_any_shared_owner():
            raise q_exc.PortRequiresDisassociation()

        db_api.update_port_associations_for_ip(context, [], ip_address)

        ipam_driver.deallocate_ip_address(context, ip_address)