def delete_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Removes the load balancer from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id), method='DELETE')

        return response