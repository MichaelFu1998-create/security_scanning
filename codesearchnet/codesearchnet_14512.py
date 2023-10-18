def create_lan(self, datacenter_id, lan):
        """
        Creates a LAN in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan: The LAN object to be created.
        :type       lan: ``dict``

        """
        data = json.dumps(self._create_lan_dict(lan))

        response = self._perform_request(
            url='/datacenters/%s/lans' % datacenter_id,
            method='POST',
            data=data)

        return response