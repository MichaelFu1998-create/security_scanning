def remove_group_user(self, group_id, user_id):
        """
        Removes a user from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s/users/%s' % (group_id, user_id),
            method='DELETE')

        return response