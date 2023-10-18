def folder_get(self, token, folder_id):
        """
        Get the attributes of the specified folder.

        :param token: A valid token for the user in question.
        :type token: string
        :param folder_id: The id of the requested folder.
        :type folder_id: int | long
        :returns: Dictionary of the folder attributes.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = folder_id
        response = self.request('midas.folder.get', parameters)
        return response