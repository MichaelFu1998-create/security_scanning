def update_lan(self, datacenter_id, lan_id, name=None,
                   public=None, ip_failover=None):
        """
        Updates a LAN

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        :param      name: The new name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      ip_failover: A list of IP fail-over dicts.
        :type       ip_failover: ``list``

        """
        data = {}

        if name:
            data['name'] = name

        if public is not None:
            data['public'] = public

        if ip_failover:
            data['ipFailover'] = ip_failover

        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (datacenter_id, lan_id),
            method='PATCH',
            data=json.dumps(data))

        return response