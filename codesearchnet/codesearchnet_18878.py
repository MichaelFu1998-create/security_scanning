def get_user_by_name(self, firstname, lastname):
        """
        Get a user by the first and last name of that user.

        :param firstname: The first name of the user.
        :type firstname: string
        :param lastname: The last name of the user.
        :type lastname: string
        :returns: The user requested.
        :rtype: dict
        """
        parameters = dict()
        parameters['firstname'] = firstname
        parameters['lastname'] = lastname
        response = self.request('midas.user.get', parameters)
        return response