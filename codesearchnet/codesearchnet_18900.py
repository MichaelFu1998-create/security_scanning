def search_item_by_name_and_folder_name(self, name, folder_name,
                                            token=None):
        """
        Return all items with a given name and parent folder name.

        :param name: The name of the item to search by.
        :type name: string
        :param folder_name: The name of the parent folder to search by.
        :type folder_name: string
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: A list of all items with the given name and parent folder
            name.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['name'] = name
        parameters['folderName'] = folder_name
        if token:
            parameters['token'] = token
        response = self.request('midas.item.searchbynameandfoldername',
                                parameters)
        return response['items']