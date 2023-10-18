def serialize_groups(self, groups):
        """Creates a payload for the redis server

        The rule schema is the following:

        REDIS KEY - port_device_id.port_mac_address/sg
        REDIS VALUE - A JSON dump of the following:

        port_mac_address must be lower-cased and stripped of non-alphanumeric
        characters

        {"id": "<arbitrary uuid>",
          "rules": [
            {"ethertype": <hexademical integer>,
             "protocol": <integer>,
             "port start": <integer>,  # optional
             "port end": <integer>,    # optional
             "icmp type": <integer>,   # optional
             "icmp code": <integer>,   # optional
             "source network": <string>,
             "destination network": <string>,
             "action": <string>,
             "direction": <string>},
          ],
          "security groups ack": <boolean>
        }

        Example:
        {"id": "004c6369-9f3d-4d33-b8f5-9416bf3567dd",
         "rules": [
           {"ethertype": 0x800,
            "protocol": "tcp",
            "port start": 1000,
            "port end": 1999,
            "source network": "10.10.10.0/24",
            "destination network": "",
            "action": "allow",
            "direction": "ingress"},
          ],
          "security groups ack": "true"
        }

        port start/end and icmp type/code are mutually exclusive pairs.
        """
        rules = []
        for group in groups:
            rules.extend(self.serialize_rules(group.rules))
        return rules