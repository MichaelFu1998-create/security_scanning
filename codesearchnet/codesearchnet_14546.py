def reboot_server(self, datacenter_id, server_id):
        """
        Reboots the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/reboot' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response