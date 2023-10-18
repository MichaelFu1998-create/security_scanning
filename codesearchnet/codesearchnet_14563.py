def delete_user(self, user_id):
        """
        Removes a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/users/%s' % user_id,
            method='DELETE')

        return response