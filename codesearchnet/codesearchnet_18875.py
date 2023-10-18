def list_user_folders(self, token):
        """
        List the folders in the users home area.

        :param token: A valid token for the user in question.
        :type token: string
        :returns: List of dictionaries containing folder information.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['token'] = token
        response = self.request('midas.user.folders', parameters)
        return response