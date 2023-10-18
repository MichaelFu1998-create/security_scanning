def delete_datacenter(self, datacenter_id):
        """
        Removes the data center and all its components such as servers, NICs,
        load balancers, volumes.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s' % (datacenter_id),
            method='DELETE')

        return response