def _add_default_tz_bindings(self, context, switch, network_id):
        """Configure any additional default transport zone bindings."""
        default_tz = CONF.NVP.default_tz

        # If there is no default tz specified it's pointless to try
        # and add any additional default tz bindings.
        if not default_tz:
            LOG.warn("additional_default_tz_types specified, "
                     "but no default_tz. Skipping "
                     "_add_default_tz_bindings().")
            return

        # This should never be called without a neutron network uuid,
        # we require it to bind some segment allocations.
        if not network_id:
            LOG.warn("neutron network_id not specified, skipping "
                     "_add_default_tz_bindings()")
            return

        for net_type in CONF.NVP.additional_default_tz_types:
            if net_type in TZ_BINDINGS:
                binding = TZ_BINDINGS[net_type]
                binding.add(context, switch, default_tz, network_id)
            else:
                LOG.warn("Unknown default tz type %s" % (net_type))