def attach_volume(self, datacenter_id, server_id, volume_id):
        """
        Attaches a volume to a server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        data = '{ "id": "' + volume_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/volumes' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response