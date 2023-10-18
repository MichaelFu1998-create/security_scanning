def folder_children(self, token, folder_id):
        """
        Get the non-recursive children of the passed in folder_id.

        :param token: A valid token for the user in question.
        :type token: string
        :param folder_id: The id of the requested folder.
        :type folder_id: int | long
        :returns: Dictionary of two lists: 'folders' and 'items'.
        :rtype: dict[string, list]
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = folder_id
        response = self.request('midas.folder.children', parameters)
        return response