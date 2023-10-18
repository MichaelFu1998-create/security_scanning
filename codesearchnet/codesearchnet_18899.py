def search_item_by_name_and_folder(self, name, folder_id, token=None):
        """
        Return all items with a given name and parent folder id.

        :param name: The name of the item to search by.
        :type name: string
        :param folder_id: The id of the parent folder to search by.
        :type folder_id: int | long
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: A list of all items with the given name and parent folder id.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['name'] = name
        parameters['folderId'] = folder_id
        if token:
            parameters['token'] = token
        response = self.request('midas.item.searchbynameandfolder', parameters)
        return response['items']