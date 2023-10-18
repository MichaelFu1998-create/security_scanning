def get_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Retrieves a single load balancer by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id))

        return response