def apply_rules(self, device_id, mac_address, rules):
        """Writes a series of security group rules to a redis server."""
        LOG.info("Applying security group rules for device %s with MAC %s" %
                 (device_id, mac_address))

        rule_dict = {SECURITY_GROUP_RULE_KEY: rules}
        redis_key = self.vif_key(device_id, mac_address)
        # TODO(mdietz): Pipeline these. Requires some rewriting
        self.set_field(redis_key, SECURITY_GROUP_HASH_ATTR, rule_dict)
        self.set_field_raw(redis_key, SECURITY_GROUP_ACK, False)