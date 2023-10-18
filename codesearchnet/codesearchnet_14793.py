def _validate_allocation_pools(self):
        """Validate IP allocation pools.

        Verify start and end address for each allocation pool are valid,
        ie: constituted by valid and appropriately ordered IP addresses.
        Also, verify pools do not overlap among themselves.
        Finally, verify that each range fall within the subnet's CIDR.
        """
        ip_pools = self._alloc_pools
        subnet_cidr = self._subnet_cidr

        LOG.debug(_("Performing IP validity checks on allocation pools"))
        ip_sets = []
        for ip_pool in ip_pools:
            try:
                start_ip = netaddr.IPAddress(ip_pool['start'])
                end_ip = netaddr.IPAddress(ip_pool['end'])
            except netaddr.AddrFormatError:
                LOG.info(_("Found invalid IP address in pool: "
                           "%(start)s - %(end)s:"),
                         {'start': ip_pool['start'],
                          'end': ip_pool['end']})
                raise n_exc_ext.InvalidAllocationPool(pool=ip_pool)
            if (start_ip.version != self._subnet_cidr.version or
                    end_ip.version != self._subnet_cidr.version):
                LOG.info(_("Specified IP addresses do not match "
                           "the subnet IP version"))
                raise n_exc_ext.InvalidAllocationPool(pool=ip_pool)
            if end_ip < start_ip:
                LOG.info(_("Start IP (%(start)s) is greater than end IP "
                           "(%(end)s)"),
                         {'start': ip_pool['start'], 'end': ip_pool['end']})
                raise n_exc_ext.InvalidAllocationPool(pool=ip_pool)
            if (start_ip < self._subnet_first_ip or
                    end_ip > self._subnet_last_ip):
                LOG.info(_("Found pool larger than subnet "
                           "CIDR:%(start)s - %(end)s"),
                         {'start': ip_pool['start'],
                          'end': ip_pool['end']})
                raise n_exc_ext.OutOfBoundsAllocationPool(
                    pool=ip_pool,
                    subnet_cidr=subnet_cidr)
            # Valid allocation pool
            # Create an IPSet for it for easily verifying overlaps
            ip_sets.append(netaddr.IPSet(netaddr.IPRange(
                ip_pool['start'],
                ip_pool['end']).cidrs()))

        LOG.debug(_("Checking for overlaps among allocation pools "
                    "and gateway ip"))
        ip_ranges = ip_pools[:]

        # Use integer cursors as an efficient way for implementing
        # comparison and avoiding comparing the same pair twice
        for l_cursor in xrange(len(ip_sets)):
            for r_cursor in xrange(l_cursor + 1, len(ip_sets)):
                if ip_sets[l_cursor] & ip_sets[r_cursor]:
                    l_range = ip_ranges[l_cursor]
                    r_range = ip_ranges[r_cursor]
                    LOG.info(_("Found overlapping ranges: %(l_range)s and "
                               "%(r_range)s"),
                             {'l_range': l_range, 'r_range': r_range})
                    raise n_exc_ext.OverlappingAllocationPools(
                        pool_1=l_range,
                        pool_2=r_range,
                        subnet_cidr=subnet_cidr)