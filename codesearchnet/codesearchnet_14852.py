def create_network(context, network):
    """Create a network.

    Create a network which represents an L2 network segment which
    can have a set of subnets and ports associated with it.
    : param context: neutron api request context
    : param network: dictionary describing the network, with keys
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.  All keys will be populated.
    """
    LOG.info("create_network for tenant %s" % context.tenant_id)

    with context.session.begin():
        net_attrs = network["network"]
        subs = net_attrs.pop("subnets", [])
        # Enforce subnet quotas
        if not context.is_admin:
            if len(subs) > 0:
                v4_count, v6_count = 0, 0
                for s in subs:
                    version = netaddr.IPNetwork(s['subnet']['cidr']).version
                    if version == 6:
                        v6_count += 1
                    else:
                        v4_count += 1
                if v4_count > 0:
                    tenant_q_v4 = context.session.query(qdv.Quota).filter_by(
                        tenant_id=context.tenant_id,
                        resource='v4_subnets_per_network').first()
                    if tenant_q_v4 != -1:
                        quota.QUOTAS.limit_check(
                            context,
                            context.tenant_id,
                            v4_subnets_per_network=v4_count)
                if v6_count > 0:
                    tenant_q_v6 = context.session.query(qdv.Quota).filter_by(
                        tenant_id=context.tenant_id,
                        resource='v6_subnets_per_network').first()
                    if tenant_q_v6 != -1:
                        quota.QUOTAS.limit_check(
                            context,
                            context.tenant_id,
                            v6_subnets_per_network=v6_count)
        # Generate a uuid that we're going to hand to the backend and db
        net_uuid = utils.pop_param(net_attrs, "id", None)
        net_type = None
        if net_uuid and context.is_admin:
            net = db_api.network_find(context=context, limit=None,
                                      sorts=['id'], marker=None,
                                      page_reverse=False, id=net_uuid,
                                      scope=db_api.ONE)
            net_type = utils.pop_param(net_attrs, "network_plugin", None)
            if net:
                raise q_exc.NetworkAlreadyExists(id=net_uuid)
        else:
            net_uuid = uuidutils.generate_uuid()

        # TODO(mdietz) this will be the first component registry hook, but
        #             lets make it work first
        pnet_type, phys_net, seg_id = _adapt_provider_nets(context, network)

        ipam_strategy = utils.pop_param(net_attrs, "ipam_strategy", None)
        if not ipam_strategy or not context.is_admin:
            ipam_strategy = CONF.QUARK.default_ipam_strategy

        if not ipam.IPAM_REGISTRY.is_valid_strategy(ipam_strategy):
            raise q_exc.InvalidIpamStrategy(strat=ipam_strategy)
        net_attrs["ipam_strategy"] = ipam_strategy

        # NOTE(mdietz) I think ideally we would create the providernet
        # elsewhere as a separate driver step that could be
        # kept in a plugin and completely removed if desired. We could
        # have a pre-callback/observer on the netdriver create_network
        # that gathers any additional parameters from the network dict

        default_net_type = net_type or CONF.QUARK.default_network_type
        net_driver = registry.DRIVER_REGISTRY.get_driver(default_net_type)
        net_driver.create_network(context, net_attrs["name"],
                                  network_id=net_uuid, phys_type=pnet_type,
                                  phys_net=phys_net, segment_id=seg_id)

        net_attrs["id"] = net_uuid
        net_attrs["tenant_id"] = context.tenant_id
        net_attrs["network_plugin"] = default_net_type
        new_net = db_api.network_create(context, **net_attrs)

        new_subnets = []
        for sub in subs:
            sub["subnet"]["network_id"] = new_net["id"]
            sub["subnet"]["tenant_id"] = context.tenant_id
            s = db_api.subnet_create(context, **sub["subnet"])
            new_subnets.append(s)
        new_net["subnets"] = new_subnets

        # if not security_groups.get_security_groups(
        #        context,
        #        filters={"id": security_groups.DEFAULT_SG_UUID}):
        #    security_groups._create_default_security_group(context)
    return v._make_network_dict(new_net)