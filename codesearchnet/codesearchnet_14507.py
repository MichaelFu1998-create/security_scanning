def delete_ipblock(self, ipblock_id):
        """
        Removes a single IP block from your account.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request(
            url='/ipblocks/' + ipblock_id, method='DELETE')

        return response