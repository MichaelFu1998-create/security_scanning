def create_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule):
        """
        Creates a firewall rule on the specified NIC and server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule: A firewall rule dict.
        :type       firewall_rule: ``dict``

        """
        properties = {
            "name": firewall_rule.name
        }

        if firewall_rule.protocol:
            properties['protocol'] = firewall_rule.protocol

        # Optional Properties
        if firewall_rule.source_mac:
            properties['sourceMac'] = firewall_rule.source_mac

        if firewall_rule.source_ip:
            properties['sourceIp'] = firewall_rule.source_ip

        if firewall_rule.target_ip:
            properties['targetIp'] = firewall_rule.target_ip

        if firewall_rule.port_range_start:
            properties['portRangeStart'] = firewall_rule.port_range_start

        if firewall_rule.port_range_end:
            properties['portRangeEnd'] = firewall_rule.port_range_end

        if firewall_rule.icmp_type:
            properties['icmpType'] = firewall_rule.icmp_type

        if firewall_rule.icmp_code:
            properties['icmpCode'] = firewall_rule.icmp_code

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules' % (
                datacenter_id,
                server_id,
                nic_id),
            method='POST',
            data=json.dumps(data))

        return response