def serialize_rules(self, rules):
        """Creates a payload for the redis server."""
        # TODO(mdietz): If/when we support other rule types, this comment
        #               will have to be revised.
        # Action and direction are static, for now. The implementation may
        # support 'deny' and 'egress' respectively in the future. We allow
        # the direction to be set to something else, technically, but current
        # plugin level call actually raises. It's supported here for unit
        # test purposes at this time
        serialized = []
        for rule in rules:
            direction = rule["direction"]
            source = ''
            destination = ''
            if rule.get("remote_ip_prefix"):
                prefix = rule["remote_ip_prefix"]
                if direction == "ingress":
                    source = self._convert_remote_network(prefix)
                else:
                    if (Capabilities.EGRESS not in
                            CONF.QUARK.environment_capabilities):
                        raise q_exc.EgressSecurityGroupRulesNotEnabled()
                    else:
                        destination = self._convert_remote_network(prefix)

            optional_fields = {}

            # NOTE(mdietz): this will expand as we add more protocols
            protocol_map = protocols.PROTOCOL_MAP[rule["ethertype"]]
            if rule["protocol"] == protocol_map["icmp"]:
                optional_fields["icmp type"] = rule["port_range_min"]
                optional_fields["icmp code"] = rule["port_range_max"]
            else:
                optional_fields["port start"] = rule["port_range_min"]
                optional_fields["port end"] = rule["port_range_max"]

            payload = {"ethertype": rule["ethertype"],
                       "protocol": rule["protocol"],
                       "source network": source,
                       "destination network": destination,
                       "action": "allow",
                       "direction": direction}
            payload.update(optional_fields)
            serialized.append(payload)
        return serialized