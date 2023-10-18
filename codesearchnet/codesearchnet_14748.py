def delete_port(context, id):
    """Delete a port.

    : param context: neutron api request context
    : param id: UUID representing the port to delete.
    """
    LOG.info("delete_port %s for tenant %s" % (id, context.tenant_id))

    port = db_api.port_find(context, id=id, scope=db_api.ONE)
    if not port:
        raise n_exc.PortNotFound(port_id=id)

    if 'device_id' in port:  # false is weird, but ignore that
        LOG.info("delete_port %s for tenant %s has device %s" %
                 (id, context.tenant_id, port['device_id']))

    backend_key = port["backend_key"]
    mac_address = netaddr.EUI(port["mac_address"]).value
    ipam_driver = _get_ipam_driver(port["network"], port=port)
    ipam_driver.deallocate_mac_address(context, mac_address)
    ipam_driver.deallocate_ips_by_port(
        context, port, ipam_reuse_after=CONF.QUARK.ipam_reuse_after)

    net_driver = _get_net_driver(port["network"], port=port)
    base_net_driver = _get_net_driver(port["network"])
    net_driver.delete_port(context, backend_key, device_id=port["device_id"],
                           mac_address=port["mac_address"],
                           base_net_driver=base_net_driver)

    with context.session.begin():
        db_api.port_delete(context, port)