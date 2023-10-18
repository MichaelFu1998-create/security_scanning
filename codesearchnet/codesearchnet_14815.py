def _get_base_network_info(self, context, network_id, base_net_driver):
        """Return a dict of extra network information.

        :param context: neutron request context.
        :param network_id: neturon network id.
        :param net_driver: network driver associated with network_id.
        :raises IronicException: Any unexpected data fetching failures will
            be logged and IronicException raised.

        This driver can attach to networks managed by other drivers. We may
        need some information from these drivers, or otherwise inform
        downstream about the type of network we are attaching to. We can
        make these decisions here.
        """
        driver_name = base_net_driver.get_name()
        net_info = {"network_type": driver_name}
        LOG.debug('_get_base_network_info: %s %s'
                  % (driver_name, network_id))

        # If the driver is NVP, we need to look up the lswitch id we should
        # be attaching to.
        if driver_name == 'NVP':
            LOG.debug('looking up lswitch ids for network %s'
                      % (network_id))
            lswitch_ids = base_net_driver.get_lswitch_ids_for_network(
                context, network_id)

            if not lswitch_ids or len(lswitch_ids) > 1:
                msg = ('lswitch id lookup failed, %s ids found.'
                       % (len(lswitch_ids)))
                LOG.error(msg)
                raise IronicException(msg)

            lswitch_id = lswitch_ids.pop()
            LOG.info('found lswitch for network %s: %s'
                     % (network_id, lswitch_id))
            net_info['lswitch_id'] = lswitch_id

        LOG.debug('_get_base_network_info finished: %s %s %s'
                  % (driver_name, network_id, net_info))
        return net_info