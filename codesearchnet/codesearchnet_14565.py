def add_group_user(self, group_id, user_id):
        """
        Adds an existing user to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        data = {
            "id": user_id
        }

        response = self._perform_request(
            url='/um/groups/%s/users' % group_id,
            method='POST',
            data=json.dumps(data))

        return response