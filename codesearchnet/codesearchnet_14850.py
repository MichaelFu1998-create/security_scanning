def get_interfaces(self):
        """Returns a set of VIFs from `get_instances` return value."""
        LOG.debug("Getting interfaces from Xapi")

        with self.sessioned() as session:
            instances = self.get_instances(session)
            recs = session.xenapi.VIF.get_all_records()

        interfaces = set()
        for vif_ref, rec in recs.iteritems():
            vm = instances.get(rec["VM"])
            if not vm:
                continue
            device_id = vm.uuid
            interfaces.add(VIF(device_id, rec, vif_ref))
        return interfaces