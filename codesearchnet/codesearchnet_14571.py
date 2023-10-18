def delete_volume(self, datacenter_id, volume_id):
        """
        Removes a volume from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/volumes/%s' % (
                datacenter_id, volume_id), method='DELETE')

        return response