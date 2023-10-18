def attach_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Attaches a CDROM to a server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        data = '{ "id": "' + cdrom_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/cdroms' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response