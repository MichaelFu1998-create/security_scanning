def get_user_by_id(self, user_id):
        """
        Get a user by the first and last name of that user.

        :param user_id: The id of the desired user.
        :type user_id: int | long
        :returns: The user requested.
        :rtype: dict
        """
        parameters = dict()
        parameters['user_id'] = user_id
        response = self.request('midas.user.get', parameters)
        return response