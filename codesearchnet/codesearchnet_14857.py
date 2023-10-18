def delete_network(context, id):
    """Delete a network.

    : param context: neutron api request context
    : param id: UUID representing the network to delete.
    """
    LOG.info("delete_network %s for tenant %s" % (id, context.tenant_id))
    with context.session.begin():
        net = db_api.network_find(context=context, limit=None, sorts=['id'],
                                  marker=None, page_reverse=False, id=id,
                                  scope=db_api.ONE)
        if not net:
            raise n_exc.NetworkNotFound(net_id=id)
        if not context.is_admin:
            if STRATEGY.is_provider_network(net.id):
                raise n_exc.NotAuthorized(net_id=id)
        if net.ports:
            raise n_exc.NetworkInUse(net_id=id)
        net_driver = registry.DRIVER_REGISTRY.get_driver(net["network_plugin"])
        net_driver.delete_network(context, id)
        for subnet in net["subnets"]:
            subnets._delete_subnet(context, subnet)
        db_api.network_delete(context, net)