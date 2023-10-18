def get_default_api_key(self, email, password):
        """
        Get the default API key for a user.

        :param email: The email of the user.
        :type email: string
        :param password: The user's password.
        :type password: string
        :returns: API key to confirm that it was fetched successfully.
        :rtype: string
        """
        parameters = dict()
        parameters['email'] = email
        parameters['password'] = password
        response = self.request('midas.user.apikey.default', parameters)
        return response['apikey']