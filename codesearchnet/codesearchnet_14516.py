def list_loadbalancers(self, datacenter_id, depth=1):
        """
        Retrieves a list of load balancers in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers?depth=%s' % (
                datacenter_id, str(depth)))

        return response