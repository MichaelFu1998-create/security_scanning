def select_ipam_strategy(self, network_id, network_strategy, **kwargs):
        """Return relevant IPAM strategy name.

        :param network_id: neutron network id.
        :param network_strategy: default strategy for the network.

        NOTE(morgabra) This feels like a hack but I can't think of a better
        idea. The root problem is we can now attach ports to networks with
        a different backend driver/ipam strategy than the network speficies.

        We handle the the backend driver part with allowing network_plugin to
        be specified for port objects. This works pretty well because nova or
        whatever knows when we are hooking up an Ironic node so it can pass
        along that key during port_create().

        IPAM is a little trickier, especially in Ironic's case, because we
        *must* use a specific IPAM for provider networks. There isn't really
        much of an option other than involve the backend driver when selecting
        the IPAM strategy.
        """
        LOG.info("Selecting IPAM strategy for network_id:%s "
                 "network_strategy:%s" % (network_id, network_strategy))

        net_type = "tenant"
        if STRATEGY.is_provider_network(network_id):
            net_type = "provider"

        strategy = self._ipam_strategies.get(net_type, {})
        default = strategy.get("default")
        overrides = strategy.get("overrides", {})

        # If we override a particular strategy explicitly, we use it.
        if network_strategy in overrides:
            LOG.info("Selected overridden IPAM strategy: %s"
                     % (overrides[network_strategy]))
            return overrides[network_strategy]

        # Otherwise, we are free to use an explicit default.
        if default:
            LOG.info("Selected default IPAM strategy for tenant "
                     "network: %s" % (default))
            return default

        # Fallback to the network-specified IPAM strategy
        LOG.info("Selected network strategy for tenant "
                 "network: %s" % (network_strategy))
        return network_strategy