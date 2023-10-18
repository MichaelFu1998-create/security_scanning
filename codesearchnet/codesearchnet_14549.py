def create_snapshot(self, datacenter_id, volume_id,
                        name=None, description=None):
        """
        Creates a snapshot of the specified volume.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        :param      name: The name given to the volume.
        :type       name: ``str``

        :param      description: The description given to the volume.
        :type       description: ``str``

        """

        data = {'name': name, 'description': description}

        response = self._perform_request(
            '/datacenters/%s/volumes/%s/create-snapshot' % (
                datacenter_id, volume_id),
            method='POST-ACTION-JSON',
            data=urlencode(data))

        return response