def get_group(self, group_id, depth=1):
        """
        Retrieves a single group by ID.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s?depth=%s' % (group_id, str(depth)))

        return response