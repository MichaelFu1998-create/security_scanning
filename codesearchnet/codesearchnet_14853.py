def update_network(context, id, network):
    """Update values of a network.

    : param context: neutron api request context
    : param id: UUID representing the network to update.
    : param network: dictionary with keys indicating fields to update.
        valid keys are those that have a value of True for 'allow_put'
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.
    """
    LOG.info("update_network %s for tenant %s" %
             (id, context.tenant_id))
    with context.session.begin():
        net = db_api.network_find(context, id=id, scope=db_api.ONE)
        if not net:
            raise n_exc.NetworkNotFound(net_id=id)
        net_dict = network["network"]
        utils.pop_param(net_dict, "network_plugin")
        if not context.is_admin and "ipam_strategy" in net_dict:
            utils.pop_param(net_dict, "ipam_strategy")
        net = db_api.network_update(context, net, **net_dict)

    return v._make_network_dict(net)