def delete_lan(self, datacenter_id, lan_id):
        """
        Removes a LAN from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (
                datacenter_id, lan_id), method='DELETE')

        return response