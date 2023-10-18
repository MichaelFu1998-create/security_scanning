def get_security_group_states(self, interfaces):
        """Gets security groups for interfaces from Redis

        Returns a dictionary of xapi.VIFs with values of the current
        acknowledged status in Redis.

        States not explicitly handled:
        * ack key, no rules - This is the same as just tagging the VIF,
          the instance will be inaccessible
        * rules key, no ack - Nothing will happen, the VIF will
          not be tagged.
        """
        LOG.debug("Getting security groups from Redis for {0}".format(
            interfaces))
        interfaces = tuple(interfaces)
        vif_keys = [self.vif_key(vif.device_id, vif.mac_address)
                    for vif in interfaces]

        # Retrieve all fields associated with this key, which should be
        # 'security groups ack' and 'security group rules'.
        sec_grp_all = self.get_fields_all(vif_keys)

        ret = {}
        # Associate the vif with the fields in a dictionary
        for vif, group in zip(interfaces, sec_grp_all):
            if group:
                ret[vif] = {SECURITY_GROUP_ACK: None,
                            SECURITY_GROUP_HASH_ATTR: []}
                temp_ack = group[SECURITY_GROUP_ACK].lower()
                temp_rules = group[SECURITY_GROUP_HASH_ATTR]
                if temp_rules:
                    temp_rules = json.loads(temp_rules)
                    ret[vif][SECURITY_GROUP_HASH_ATTR] = temp_rules["rules"]
                if "true" in temp_ack:
                    ret[vif][SECURITY_GROUP_ACK] = True
                elif "false" in temp_ack:
                    ret[vif][SECURITY_GROUP_ACK] = False
                else:
                    ret.pop(vif, None)
                    LOG.debug("Skipping bad ack value %s" % temp_ack)

        return ret