def delete_share(self, group_id, resource_id):
        """
        Removes a resource share from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s/shares/%s' % (group_id, resource_id),
            method='DELETE')

        return response