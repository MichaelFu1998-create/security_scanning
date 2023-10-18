def get_firewall_rule(self, datacenter_id,
                          server_id, nic_id, firewall_rule_id):
        """
        Retrieves a single firewall rule by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the firewall rule.
        :type       firewall_rule_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id))

        return response