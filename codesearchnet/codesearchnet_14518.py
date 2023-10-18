def create_loadbalancer(self, datacenter_id, loadbalancer):
        """
        Creates a load balancer within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer: The load balancer object to be created.
        :type       loadbalancer: ``dict``

        """
        data = json.dumps(self._create_loadbalancer_dict(loadbalancer))

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers' % datacenter_id,
            method='POST',
            data=data)

        return response