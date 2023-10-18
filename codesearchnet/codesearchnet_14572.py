def create_volume(self, datacenter_id, volume):
        """
        Creates a volume within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume: A volume dict.
        :type       volume: ``dict``

        """

        data = (json.dumps(self._create_volume_dict(volume)))

        response = self._perform_request(
            url='/datacenters/%s/volumes' % datacenter_id,
            method='POST',
            data=data)

        return response