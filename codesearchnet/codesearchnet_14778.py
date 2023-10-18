def update_subnet(context, id, subnet):
    """Update values of a subnet.

    : param context: neutron api request context
    : param id: UUID representing the subnet to update.
    : param subnet: dictionary with keys indicating fields to update.
        valid keys are those that have a value of True for 'allow_put'
        as listed in the RESOURCE_ATTRIBUTE_MAP object in
        neutron/api/v2/attributes.py.
    """
    LOG.info("update_subnet %s for tenant %s" %
             (id, context.tenant_id))

    with context.session.begin():
        subnet_db = db_api.subnet_find(context=context, limit=None,
                                       page_reverse=False, sorts=['id'],
                                       marker_obj=None, fields=None,
                                       id=id, scope=db_api.ONE)
        if not subnet_db:
            raise n_exc.SubnetNotFound(subnet_id=id)

        s = subnet["subnet"]
        always_pop = ["_cidr", "cidr", "first_ip", "last_ip", "ip_version",
                      "segment_id", "network_id"]
        admin_only = ["do_not_use", "created_at", "tenant_id",
                      "next_auto_assign_ip", "enable_dhcp"]
        utils.filter_body(context, s, admin_only, always_pop)

        dns_ips = utils.pop_param(s, "dns_nameservers", [])
        host_routes = utils.pop_param(s, "host_routes", [])
        gateway_ip = utils.pop_param(s, "gateway_ip", None)
        allocation_pools = utils.pop_param(s, "allocation_pools", None)
        if not CONF.QUARK.allow_allocation_pool_update:
            if allocation_pools:
                raise n_exc.BadRequest(
                    resource="subnets",
                    msg="Allocation pools cannot be updated.")

            if subnet_db["ip_policy"] is not None:
                ip_policy_cidrs = subnet_db["ip_policy"].get_cidrs_ip_set()
            else:
                ip_policy_cidrs = netaddr.IPSet([])

            alloc_pools = allocation_pool.AllocationPools(
                subnet_db["cidr"],
                policies=ip_policy_cidrs)
        else:
            alloc_pools = allocation_pool.AllocationPools(subnet_db["cidr"],
                                                          allocation_pools)
            original_pools = subnet_db.allocation_pools
            ori_pools = allocation_pool.AllocationPools(subnet_db["cidr"],
                                                        original_pools)
            # Check if the pools are growing or shrinking
            is_growing = _pool_is_growing(ori_pools, alloc_pools)
            if not CONF.QUARK.allow_allocation_pool_growth and is_growing:
                raise n_exc.BadRequest(
                    resource="subnets",
                    msg="Allocation pools may not be updated to be larger "
                        "do to configuration settings")

        quota.QUOTAS.limit_check(
            context,
            context.tenant_id,
            alloc_pools_per_subnet=len(alloc_pools))
        if gateway_ip:
            alloc_pools.validate_gateway_excluded(gateway_ip)
            default_route = None
            for route in host_routes:
                netaddr_route = netaddr.IPNetwork(route["destination"])
                if netaddr_route.value == routes.DEFAULT_ROUTE.value:
                    default_route = route
                    break

            if default_route is None:
                route_model = db_api.route_find(
                    context, cidr=str(routes.DEFAULT_ROUTE), subnet_id=id,
                    scope=db_api.ONE)
                if route_model:
                    db_api.route_update(context, route_model,
                                        gateway=gateway_ip)
                else:
                    db_api.route_create(context,
                                        cidr=str(routes.DEFAULT_ROUTE),
                                        gateway=gateway_ip, subnet_id=id)

        if dns_ips:
            subnet_db["dns_nameservers"] = []
            quota.QUOTAS.limit_check(context, context.tenant_id,
                                     dns_nameservers_per_subnet=len(dns_ips))

        for dns_ip in dns_ips:
            subnet_db["dns_nameservers"].append(db_api.dns_create(
                context,
                ip=netaddr.IPAddress(dns_ip)))

        if host_routes:
            subnet_db["routes"] = []
            quota.QUOTAS.limit_check(context, context.tenant_id,
                                     routes_per_subnet=len(host_routes))

        for route in host_routes:
            subnet_db["routes"].append(db_api.route_create(
                context, cidr=route["destination"], gateway=route["nexthop"]))
        if CONF.QUARK.allow_allocation_pool_update:
            if isinstance(allocation_pools, list):
                cidrs = alloc_pools.get_policy_cidrs()
                ip_policies.ensure_default_policy(cidrs, [subnet_db])
                subnet_db["ip_policy"] = db_api.ip_policy_update(
                    context, subnet_db["ip_policy"], exclude=cidrs)
                # invalidate the cache
                db_api.subnet_update_set_alloc_pool_cache(context, subnet_db)
        subnet = db_api.subnet_update(context, subnet_db, **s)
    return v._make_subnet_dict(subnet)