def _allocate_from_v6_subnet(self, context, net_id, subnet,
                                 port_id, reuse_after, ip_address=None,
                                 **kwargs):
        """This attempts to allocate v6 addresses as per RFC2462 and RFC3041.

        To accomodate this, we effectively treat all v6 assignment as a
        first time allocation utilizing the MAC address of the VIF. Because
        we recycle MACs, we will eventually attempt to recreate a previously
        generated v6 address. Instead of failing, we've opted to handle
        reallocating that address in this method.

        This should provide a performance boost over attempting to check
        each and every subnet in the existing reallocate logic, as we'd
        have to iterate over each and every subnet returned
        """

        LOG.info("Attempting to allocate a v6 address - [{0}]".format(
            utils.pretty_kwargs(network_id=net_id, subnet=subnet,
                                port_id=port_id, ip_address=ip_address)))

        if ip_address:
            LOG.info("IP %s explicitly requested, deferring to standard "
                     "allocation" % ip_address)
            return self._allocate_from_subnet(context, net_id=net_id,
                                              subnet=subnet, port_id=port_id,
                                              reuse_after=reuse_after,
                                              ip_address=ip_address, **kwargs)
        else:
            mac = kwargs.get("mac_address")
            if mac:
                mac = kwargs["mac_address"].get("address")

            if subnet and subnet["ip_policy"]:
                ip_policy_cidrs = subnet["ip_policy"].get_cidrs_ip_set()
            else:
                ip_policy_cidrs = netaddr.IPSet([])

            for tries, ip_address in enumerate(
                    generate_v6(mac, port_id, subnet["cidr"])):

                LOG.info("Attempt {0} of {1}".format(
                    tries + 1, CONF.QUARK.v6_allocation_attempts))

                if tries > CONF.QUARK.v6_allocation_attempts - 1:
                    LOG.info("Exceeded v6 allocation attempts, bailing")
                    raise ip_address_failure(net_id)

                ip_address = netaddr.IPAddress(ip_address).ipv6()
                LOG.info("Generated a new v6 address {0}".format(
                    str(ip_address)))

                if (ip_policy_cidrs is not None and
                        ip_address in ip_policy_cidrs):
                    LOG.info("Address {0} excluded by policy".format(
                        str(ip_address)))
                    continue

                try:
                    with context.session.begin():
                        address = db_api.ip_address_create(
                            context, address=ip_address,
                            subnet_id=subnet["id"],
                            version=subnet["ip_version"], network_id=net_id,
                            address_type=kwargs.get('address_type',
                                                    ip_types.FIXED))
                        return address
                except db_exception.DBDuplicateEntry:
                    # This shouldn't ever happen, since we hold a unique MAC
                    # address from the previous IPAM step.
                    LOG.info("{0} exists but was already "
                             "allocated".format(str(ip_address)))
                    LOG.debug("Duplicate entry found when inserting subnet_id"
                              " %s ip_address %s", subnet["id"], ip_address)