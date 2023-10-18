def add_loadbalanced_nics(self, datacenter_id,
                              loadbalancer_id, nic_id):
        """
        Associates a NIC with the given load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The ID of the NIC.
        :type       nic_id: ``str``

        """
        data = '{ "id": "' + nic_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics' % (
                datacenter_id,
                loadbalancer_id),
            method='POST',
            data=data)

        return response