def update_user(self, user_id, **kwargs):
        """
        Updates a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        properties = {}

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/users/%s' % user_id,
            method='PUT',
            data=json.dumps(data))

        return response