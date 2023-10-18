def create_nic(self, datacenter_id, server_id, nic):
        """
        Creates a NIC on the specified server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic: A NIC dict.
        :type       nic: ``dict``

        """

        data = json.dumps(self._create_nic_dict(nic))

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response