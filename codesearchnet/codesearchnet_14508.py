def reserve_ipblock(self, ipblock):
        """
        Reserves an IP block within your account.

        """
        properties = {
            "name": ipblock.name
        }

        if ipblock.location:
            properties['location'] = ipblock.location

        if ipblock.size:
            properties['size'] = str(ipblock.size)

        raw = {
            "properties": properties,
        }

        response = self._perform_request(
            url='/ipblocks', method='POST', data=json.dumps(raw))

        return response