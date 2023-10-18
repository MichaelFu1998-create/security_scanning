def delete_group(self, group_id):
        """
        Removes a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s' % group_id,
            method='DELETE')

        return response