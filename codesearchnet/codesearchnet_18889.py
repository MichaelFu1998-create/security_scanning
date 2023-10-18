def move_folder(self, token, folder_id, dest_folder_id):
        """
        Move a folder to the destination folder.

        :param token: A valid token for the user in question.
        :type token: string
        :param folder_id: The id of the folder to be moved.
        :type folder_id: int | long
        :param dest_folder_id: The id of destination (new parent) folder.
        :type dest_folder_id: int | long
        :returns: Dictionary containing the details of the moved folder.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = folder_id
        parameters['dstfolderid'] = dest_folder_id
        response = self.request('midas.folder.move', parameters)
        return response