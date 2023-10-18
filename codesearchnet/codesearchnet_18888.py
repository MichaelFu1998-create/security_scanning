def delete_folder(self, token, folder_id):
        """
        Delete the folder with the passed in folder_id.

        :param token: A valid token for the user in question.
        :type token: string
        :param folder_id: The id of the folder to be deleted.
        :type folder_id: int | long
        :returns: None.
        :rtype: None
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = folder_id
        response = self.request('midas.folder.delete', parameters)
        return response