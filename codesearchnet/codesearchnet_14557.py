def get_share(self, group_id, resource_id, depth=1):
        """
        Retrieves a specific resource share available to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s/shares/%s?depth=%s'
            % (group_id, resource_id, str(depth)))

        return response