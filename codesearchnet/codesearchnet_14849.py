def get_instances(self, session):
        """Returns a dict of `VM OpaqueRef` (str) -> `xapi.VM`."""
        LOG.debug("Getting instances from Xapi")

        recs = session.xenapi.VM.get_all_records()

        # NOTE(asadoughi): Copied from xen-networking-scripts/utils.py
        is_inst = lambda r: (r['power_state'].lower() == 'running' and
                             not r['is_a_template'] and
                             not r['is_control_domain'] and
                             ('nova_uuid' in r['other_config'] or
                              r['name_label'].startswith('instance-')))
        instances = dict()
        for vm_ref, rec in recs.iteritems():
            if not is_inst(rec):
                continue
            instances[vm_ref] = VM(ref=vm_ref,
                                   uuid=rec["other_config"]["nova_uuid"],
                                   vifs=rec["VIFs"],
                                   dom_id=rec["domid"])
        return instances