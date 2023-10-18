def create_user(self, user):
        """
        Creates a new user.

        :param      user: The user object to be created.
        :type       user: ``dict``

        """
        data = self._create_user_dict(user=user)

        response = self._perform_request(
            url='/um/users',
            method='POST',
            data=json.dumps(data))

        return response