def update_port(context, id, port):
    """Update values of a port.

    : param context: neutron api request context
    : param id: UUID representing the port to update.
    : param port: dictionary with keys indicating fields to update.
        valid keys are those that have a value of True for 'allow_put'
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.
    """
    LOG.info("update_port %s for tenant %s" % (id, context.tenant_id))
    port_db = db_api.port_find(context, id=id, scope=db_api.ONE)
    if not port_db:
        raise n_exc.PortNotFound(port_id=id)

    port_dict = port["port"]
    fixed_ips = port_dict.pop("fixed_ips", None)

    admin_only = ["mac_address", "device_owner", "bridge", "admin_state_up",
                  "device_id"]
    always_filter = ["network_id", "backend_key", "network_plugin"]
    utils.filter_body(context, port_dict, admin_only=admin_only,
                      always_filter=always_filter)

    # Pre-check the requested fixed_ips before making too many db trips.
    # Note that this is the only check we need, since this call replaces
    # the entirety of the IP addresses document if fixed_ips are provided.
    if fixed_ips:
        quota.QUOTAS.limit_check(context, context.tenant_id,
                                 fixed_ips_per_port=len(fixed_ips))

    new_security_groups = utils.pop_param(port_dict, "security_groups")
    if new_security_groups is not None:
        if (Capabilities.TENANT_NETWORK_SG not in
                CONF.QUARK.environment_capabilities):
            if not STRATEGY.is_provider_network(port_db["network_id"]):
                raise q_exc.TenantNetworkSecurityGroupRulesNotEnabled()

    if new_security_groups is not None and not port_db["device_id"]:
        raise q_exc.SecurityGroupsRequireDevice()

    group_ids, security_group_mods = _make_security_group_list(
        context, new_security_groups)
    quota.QUOTAS.limit_check(context, context.tenant_id,
                             security_groups_per_port=len(group_ids))

    if fixed_ips is not None:
        # NOTE(mdietz): we want full control over IPAM since
        #              we're allocating by subnet instead of
        #              network.
        ipam_driver = ipam.IPAM_REGISTRY.get_strategy(
            ipam.QuarkIpamANY.get_name())

        addresses, subnet_ids = [], []
        ip_addresses = {}

        for fixed_ip in fixed_ips:
            subnet_id = fixed_ip.get("subnet_id")
            ip_address = fixed_ip.get("ip_address")
            if not (subnet_id or ip_address):
                raise n_exc.BadRequest(
                    resource="fixed_ips",
                    msg="subnet_id or ip_address required")

            if ip_address and not subnet_id:
                raise n_exc.BadRequest(
                    resource="fixed_ips",
                    msg="subnet_id required for ip_address allocation")

            if subnet_id and ip_address:
                ip_netaddr = None
                try:
                    ip_netaddr = netaddr.IPAddress(ip_address).ipv6()
                except netaddr.AddrFormatError:
                    raise n_exc.InvalidInput(
                        error_message="Invalid format provided for ip_address")
                ip_addresses[ip_netaddr] = subnet_id
            else:
                subnet_ids.append(subnet_id)

        port_ips = set([netaddr.IPAddress(int(a["address"]))
                        for a in port_db["ip_addresses"]])
        new_ips = set([a for a in ip_addresses.keys()])

        ips_to_allocate = list(new_ips - port_ips)
        ips_to_deallocate = list(port_ips - new_ips)

        for ip in ips_to_allocate:
            if ip in ip_addresses:
                # NOTE: Fix for RM10187 - we were losing the list of IPs if
                #       more than one IP was to be allocated. Track an
                #       aggregate list instead, and add it to the running total
                #       after each allocate
                allocated = []
                ipam_driver.allocate_ip_address(
                    context, allocated, port_db["network_id"],
                    port_db["id"], reuse_after=None, ip_addresses=[ip],
                    subnets=[ip_addresses[ip]])
                addresses.extend(allocated)

        for ip in ips_to_deallocate:
            ipam_driver.deallocate_ips_by_port(
                context, port_db, ip_address=ip)

        for subnet_id in subnet_ids:
            ipam_driver.allocate_ip_address(
                context, addresses, port_db["network_id"], port_db["id"],
                reuse_after=CONF.QUARK.ipam_reuse_after,
                subnets=[subnet_id])

        # Need to return all existing addresses and the new ones
        if addresses:
            port_dict["addresses"] = port_db["ip_addresses"]
            port_dict["addresses"].extend(addresses)

    # NOTE(morgabra) Updating network_plugin on port objects is explicitly
    # disallowed in the api, so we use whatever exists in the db.
    net_driver = _get_net_driver(port_db.network, port=port_db)
    base_net_driver = _get_net_driver(port_db.network)

    # TODO(anyone): What do we want to have happen here if this fails? Is it
    #               ok to continue to keep the IPs but fail to apply security
    #               groups? Is there a clean way to have a multi-status? Since
    #               we're in a beta-y status, I'm going to let this sit for
    #               a future patch where we have time to solve it well.
    kwargs = {}
    if new_security_groups is not None:
        # TODO(anyone): this is kind of silly (when testing), because it will
        #               modify the incoming dict. Probably should be a copy or
        #               something.
        kwargs["security_groups"] = security_group_mods
    net_driver.update_port(context, port_id=port_db["backend_key"],
                           mac_address=port_db["mac_address"],
                           device_id=port_db["device_id"],
                           base_net_driver=base_net_driver,
                           **kwargs)

    port_dict["security_groups"] = security_group_mods

    with context.session.begin():
        port = db_api.port_update(context, port_db, **port_dict)

    # NOTE(mdietz): fix for issue 112, we wanted the IPs to be in
    #              allocated_at order, so get a fresh object every time
    if port_db in context.session:
        context.session.expunge(port_db)
    port_db = db_api.port_find(context, id=id, scope=db_api.ONE)

    return v._make_port_dict(port_db)