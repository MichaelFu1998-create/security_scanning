def get_lan_members(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves the list of NICs that are part of the LAN.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/lans/%s/nics?depth=%s' % (
                datacenter_id,
                lan_id,
                str(depth)))

        return response