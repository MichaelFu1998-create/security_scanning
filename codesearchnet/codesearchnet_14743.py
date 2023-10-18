def create_port(context, port):
    """Create a port

    Create a port which is a connection point of a device (e.g., a VM
    NIC) to attach to a L2 Neutron network.
    : param context: neutron api request context
    : param port: dictionary describing the port, with keys
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.  All keys will be populated.
    """
    LOG.info("create_port for tenant %s" % context.tenant_id)
    port_attrs = port["port"]

    admin_only = ["mac_address", "device_owner", "bridge", "admin_state_up",
                  "use_forbidden_mac_range", "network_plugin",
                  "instance_node_id"]
    utils.filter_body(context, port_attrs, admin_only=admin_only)

    port_attrs = port["port"]
    mac_address = utils.pop_param(port_attrs, "mac_address", None)
    use_forbidden_mac_range = utils.pop_param(port_attrs,
                                              "use_forbidden_mac_range", False)
    segment_id = utils.pop_param(port_attrs, "segment_id")
    fixed_ips = utils.pop_param(port_attrs, "fixed_ips")

    if "device_id" not in port_attrs:
        port_attrs['device_id'] = ""
    device_id = port_attrs['device_id']

    # NOTE(morgabra) This should be instance.node from nova, only needed
    # for ironic_driver.
    if "instance_node_id" not in port_attrs:
        port_attrs['instance_node_id'] = ""
    instance_node_id = port_attrs['instance_node_id']

    net_id = port_attrs["network_id"]

    port_id = uuidutils.generate_uuid()

    net = db_api.network_find(context=context, limit=None, sorts=['id'],
                              marker=None, page_reverse=False, fields=None,
                              id=net_id, scope=db_api.ONE)

    if not net:
        raise n_exc.NetworkNotFound(net_id=net_id)
    _raise_if_unauthorized(context, net)

    # NOTE (Perkins): If a device_id is given, try to prevent multiple ports
    # from being created for a device already attached to the network
    if device_id:
        existing_ports = db_api.port_find(context,
                                          network_id=net_id,
                                          device_id=device_id,
                                          scope=db_api.ONE)
        if existing_ports:
            raise n_exc.BadRequest(
                resource="port", msg="This device is already connected to the "
                "requested network via another port")

    # Try to fail early on quotas and save ourselves some db overhead
    if fixed_ips:
        quota.QUOTAS.limit_check(context, context.tenant_id,
                                 fixed_ips_per_port=len(fixed_ips))

    if not STRATEGY.is_provider_network(net_id):
        # We don't honor segmented networks when they aren't "shared"
        segment_id = None
        port_count = db_api.port_count_all(context, network_id=[net_id],
                                           tenant_id=[context.tenant_id])
        quota.QUOTAS.limit_check(
            context, context.tenant_id,
            ports_per_network=port_count + 1)
    else:
        if not segment_id:
            raise q_exc.AmbiguousNetworkId(net_id=net_id)

    network_plugin = utils.pop_param(port_attrs, "network_plugin")
    if not network_plugin:
        network_plugin = net["network_plugin"]
    port_attrs["network_plugin"] = network_plugin

    ipam_driver = _get_ipam_driver(net, port=port_attrs)
    net_driver = _get_net_driver(net, port=port_attrs)
    # NOTE(morgabra) It's possible that we select a driver different than
    # the one specified by the network. However, we still might need to use
    # this for some operations, so we also fetch it and pass it along to
    # the backend driver we are actually using.
    base_net_driver = _get_net_driver(net)

    # TODO(anyone): security groups are not currently supported on port create.
    #               Please see JIRA:NCP-801
    security_groups = utils.pop_param(port_attrs, "security_groups")
    if security_groups is not None:
        raise q_exc.SecurityGroupsNotImplemented()

    group_ids, security_groups = _make_security_group_list(context,
                                                           security_groups)
    quota.QUOTAS.limit_check(context, context.tenant_id,
                             security_groups_per_port=len(group_ids))
    addresses = []
    backend_port = None

    with utils.CommandManager().execute() as cmd_mgr:
        @cmd_mgr.do
        def _allocate_ips(fixed_ips, net, port_id, segment_id, mac,
                          **kwargs):
            if fixed_ips:
                if (STRATEGY.is_provider_network(net_id) and
                        not context.is_admin):
                    raise n_exc.NotAuthorized()

                ips, subnets = split_and_validate_requested_subnets(context,
                                                                    net_id,
                                                                    segment_id,
                                                                    fixed_ips)
                kwargs["ip_addresses"] = ips
                kwargs["subnets"] = subnets

            ipam_driver.allocate_ip_address(
                context, addresses, net["id"], port_id,
                CONF.QUARK.ipam_reuse_after, segment_id=segment_id,
                mac_address=mac, **kwargs)

        @cmd_mgr.undo
        def _allocate_ips_undo(addr, **kwargs):
            LOG.info("Rolling back IP addresses...")
            if addresses:
                for address in addresses:
                    try:
                        with context.session.begin():
                            ipam_driver.deallocate_ip_address(context, address,
                                                              **kwargs)
                    except Exception:
                        LOG.exception("Couldn't release IP %s" % address)

        @cmd_mgr.do
        def _allocate_mac(net, port_id, mac_address,
                          use_forbidden_mac_range=False,
                          **kwargs):
            mac = ipam_driver.allocate_mac_address(
                context, net["id"], port_id, CONF.QUARK.ipam_reuse_after,
                mac_address=mac_address,
                use_forbidden_mac_range=use_forbidden_mac_range, **kwargs)
            return mac

        @cmd_mgr.undo
        def _allocate_mac_undo(mac, **kwargs):
            LOG.info("Rolling back MAC address...")
            if mac:
                try:
                    with context.session.begin():
                        ipam_driver.deallocate_mac_address(context,
                                                           mac["address"])
                except Exception:
                    LOG.exception("Couldn't release MAC %s" % mac)

        @cmd_mgr.do
        def _allocate_backend_port(mac, addresses, net, port_id, **kwargs):
            backend_port = net_driver.create_port(
                context, net["id"],
                port_id=port_id,
                security_groups=group_ids,
                device_id=device_id,
                instance_node_id=instance_node_id,
                mac_address=mac,
                addresses=addresses,
                base_net_driver=base_net_driver)
            _filter_backend_port(backend_port)
            return backend_port

        @cmd_mgr.undo
        def _allocate_back_port_undo(backend_port,
                                     **kwargs):
            LOG.info("Rolling back backend port...")
            try:
                backend_port_uuid = None
                if backend_port:
                    backend_port_uuid = backend_port.get("uuid")
                net_driver.delete_port(context, backend_port_uuid)
            except Exception:
                LOG.exception(
                    "Couldn't rollback backend port %s" % backend_port)

        @cmd_mgr.do
        def _allocate_db_port(port_attrs, backend_port, addresses, mac,
                              **kwargs):
            port_attrs["network_id"] = net["id"]
            port_attrs["id"] = port_id
            port_attrs["security_groups"] = security_groups

            LOG.info("Including extra plugin attrs: %s" % backend_port)
            port_attrs.update(backend_port)
            with context.session.begin():
                new_port = db_api.port_create(
                    context, addresses=addresses, mac_address=mac["address"],
                    backend_key=backend_port["uuid"], **port_attrs)

            return new_port

        @cmd_mgr.undo
        def _allocate_db_port_undo(new_port,
                                   **kwargs):
            LOG.info("Rolling back database port...")
            if not new_port:
                return
            try:
                with context.session.begin():
                    db_api.port_delete(context, new_port)
            except Exception:
                LOG.exception(
                    "Couldn't rollback db port %s" % backend_port)

        # addresses, mac, backend_port, new_port
        mac = _allocate_mac(net, port_id, mac_address,
                            use_forbidden_mac_range=use_forbidden_mac_range)
        _allocate_ips(fixed_ips, net, port_id, segment_id, mac)
        backend_port = _allocate_backend_port(mac, addresses, net, port_id)
        new_port = _allocate_db_port(port_attrs, backend_port, addresses, mac)

    return v._make_port_dict(new_port)