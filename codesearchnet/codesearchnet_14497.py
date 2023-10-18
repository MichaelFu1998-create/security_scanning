def get_datacenter(self, datacenter_id, depth=1):
        """
        Retrieves a data center by its ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s?depth=%s' % (datacenter_id, str(depth)))

        return response