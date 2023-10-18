def create_server(self, datacenter_id, server):
        """
        Creates a server within the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server: A dict of the server to be created.
        :type       server: ``dict``

        """

        data = json.dumps(self._create_server_dict(server))

        response = self._perform_request(
            url='/datacenters/%s/servers' % (datacenter_id),
            method='POST',
            data=data)

        return response