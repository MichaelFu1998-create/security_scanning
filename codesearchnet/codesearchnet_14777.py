def create_subnet(context, subnet):
    """Create a subnet.

    Create a subnet which represents a range of IP addresses
    that can be allocated to devices

    : param context: neutron api request context
    : param subnet: dictionary describing the subnet, with keys
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.  All keys will be populated.
    """
    LOG.info("create_subnet for tenant %s" % context.tenant_id)
    net_id = subnet["subnet"]["network_id"]

    with context.session.begin():
        net = db_api.network_find(context=context, limit=None, sorts=['id'],
                                  marker=None, page_reverse=False, fields=None,
                                  id=net_id, scope=db_api.ONE)
        if not net:
            raise n_exc.NetworkNotFound(net_id=net_id)

        sub_attrs = subnet["subnet"]

        always_pop = ["enable_dhcp", "ip_version", "first_ip", "last_ip",
                      "_cidr"]
        admin_only = ["segment_id", "do_not_use", "created_at",
                      "next_auto_assign_ip"]
        utils.filter_body(context, sub_attrs, admin_only, always_pop)

        _validate_subnet_cidr(context, net_id, sub_attrs["cidr"])

        cidr = netaddr.IPNetwork(sub_attrs["cidr"])

        err_vals = {'cidr': sub_attrs["cidr"], 'network_id': net_id}
        err = _("Requested subnet with cidr: %(cidr)s for "
                "network: %(network_id)s. Prefix is too small, must be a "
                "larger subnet. A prefix less than /%(prefix)s is required.")

        if cidr.version == 6 and cidr.prefixlen > 64:
            err_vals["prefix"] = 65
            err_msg = err % err_vals
            raise n_exc.InvalidInput(error_message=err_msg)
        elif cidr.version == 4 and cidr.prefixlen > 30:
            err_vals["prefix"] = 31
            err_msg = err % err_vals
            raise n_exc.InvalidInput(error_message=err_msg)
        # Enforce subnet quotas
        net_subnets = get_subnets(context,
                                  filters=dict(network_id=net_id))
        if not context.is_admin:
            v4_count, v6_count = 0, 0
            for subnet in net_subnets:
                if netaddr.IPNetwork(subnet['cidr']).version == 6:
                    v6_count += 1
                else:
                    v4_count += 1

            if cidr.version == 6:
                tenant_quota_v6 = context.session.query(qdv.Quota).filter_by(
                    tenant_id=context.tenant_id,
                    resource='v6_subnets_per_network').first()
                if tenant_quota_v6 != -1:
                    quota.QUOTAS.limit_check(
                        context, context.tenant_id,
                        v6_subnets_per_network=v6_count + 1)
            else:
                tenant_quota_v4 = context.session.query(qdv.Quota).filter_by(
                    tenant_id=context.tenant_id,
                    resource='v4_subnets_per_network').first()
                if tenant_quota_v4 != -1:
                    quota.QUOTAS.limit_check(
                        context, context.tenant_id,
                        v4_subnets_per_network=v4_count + 1)

        # See RM981. The default behavior of setting a gateway unless
        # explicitly asked to not is no longer desirable.
        gateway_ip = utils.pop_param(sub_attrs, "gateway_ip")
        dns_ips = utils.pop_param(sub_attrs, "dns_nameservers", [])
        host_routes = utils.pop_param(sub_attrs, "host_routes", [])
        allocation_pools = utils.pop_param(sub_attrs, "allocation_pools", None)

        sub_attrs["network"] = net
        new_subnet = db_api.subnet_create(context, **sub_attrs)

        cidrs = []
        alloc_pools = allocation_pool.AllocationPools(sub_attrs["cidr"],
                                                      allocation_pools)
        if isinstance(allocation_pools, list):
            cidrs = alloc_pools.get_policy_cidrs()

        quota.QUOTAS.limit_check(
            context,
            context.tenant_id,
            alloc_pools_per_subnet=len(alloc_pools))

        ip_policies.ensure_default_policy(cidrs, [new_subnet])
        new_subnet["ip_policy"] = db_api.ip_policy_create(context,
                                                          exclude=cidrs)

        quota.QUOTAS.limit_check(context, context.tenant_id,
                                 routes_per_subnet=len(host_routes))

        default_route = None
        for route in host_routes:
            netaddr_route = netaddr.IPNetwork(route["destination"])
            if netaddr_route.value == routes.DEFAULT_ROUTE.value:
                if default_route:
                    raise q_exc.DuplicateRouteConflict(
                        subnet_id=new_subnet["id"])

                default_route = route
                gateway_ip = default_route["nexthop"]
                alloc_pools.validate_gateway_excluded(gateway_ip)

            new_subnet["routes"].append(db_api.route_create(
                context, cidr=route["destination"], gateway=route["nexthop"]))

        quota.QUOTAS.limit_check(context, context.tenant_id,
                                 dns_nameservers_per_subnet=len(dns_ips))

        for dns_ip in dns_ips:
            new_subnet["dns_nameservers"].append(db_api.dns_create(
                context, ip=netaddr.IPAddress(dns_ip)))

        # if the gateway_ip is IN the cidr for the subnet and NOT excluded by
        # policies, we should raise a 409 conflict
        if gateway_ip and default_route is None:
            alloc_pools.validate_gateway_excluded(gateway_ip)
            new_subnet["routes"].append(db_api.route_create(
                context, cidr=str(routes.DEFAULT_ROUTE), gateway=gateway_ip))

    subnet_dict = v._make_subnet_dict(new_subnet)
    subnet_dict["gateway_ip"] = gateway_ip

    return subnet_dict