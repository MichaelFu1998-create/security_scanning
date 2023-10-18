def update_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule_id, **kwargs):
        """
        Updates a firewall rule.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the firewall rule.
        :type       firewall_rule_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

            if attr == 'source_mac':
                data['sourceMac'] = value
            elif attr == 'source_ip':
                data['sourceIp'] = value
            elif attr == 'target_ip':
                data['targetIp'] = value
            elif attr == 'port_range_start':
                data['portRangeStart'] = value
            elif attr == 'port_range_end':
                data['portRangeEnd'] = value
            elif attr == 'icmp_type':
                data['icmpType'] = value
            elif attr == 'icmp_code':
                data['icmpCode'] = value
            else:
                data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id),
            method='PATCH',
            data=json.dumps(data))

        return response