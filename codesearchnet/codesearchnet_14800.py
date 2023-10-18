def _remove_default_tz_bindings(self, context, network_id):
        """Deconfigure any additional default transport zone bindings."""
        default_tz = CONF.NVP.default_tz

        if not default_tz:
            LOG.warn("additional_default_tz_types specified, "
                     "but no default_tz. Skipping "
                     "_remove_default_tz_bindings().")
            return

        if not network_id:
            LOG.warn("neutron network_id not specified, skipping "
                     "_remove_default_tz_bindings()")
            return

        for net_type in CONF.NVP.additional_default_tz_types:
            if net_type in TZ_BINDINGS:
                binding = TZ_BINDINGS[net_type]
                binding.remove(context, default_tz, network_id)
            else:
                LOG.warn("Unknown default tz type %s" % (net_type))