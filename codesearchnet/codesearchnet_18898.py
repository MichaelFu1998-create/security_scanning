def search_item_by_name(self, name, token=None):
        """
        Return all items.

        :param name: The name of the item to search by.
        :type name: string
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :returns: A list of all items with the given name.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['name'] = name
        if token:
            parameters['token'] = token
        response = self.request('midas.item.searchbyname', parameters)
        return response['items']