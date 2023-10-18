def item_get(self, token, item_id):
        """
        Get the attributes of the specified item.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the requested item.
        :type item_id: int | string
        :returns: Dictionary of the item attributes.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = item_id
        response = self.request('midas.item.get', parameters)
        return response