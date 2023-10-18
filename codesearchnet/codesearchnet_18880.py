def get_user_by_email(self, email):
        """
        Get a user by the email of that user.

        :param email: The email of the desired user.
        :type email: string
        :returns: The user requested.
        :rtype: dict
        """
        parameters = dict()
        parameters['email'] = email
        response = self.request('midas.user.get', parameters)
        return response