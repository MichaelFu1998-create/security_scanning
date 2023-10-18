def get_user(self, user_id, depth=1):
        """
        Retrieves a single user by ID.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/users/%s?depth=%s' % (user_id, str(depth)))

        return response