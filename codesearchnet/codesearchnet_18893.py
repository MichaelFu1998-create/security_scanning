def delete_item(self, token, item_id):
        """
        Delete the item with the passed in item_id.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the item to be deleted.
        :type item_id: int | long
        :returns: None.
        :rtype: None
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = item_id
        response = self.request('midas.item.delete', parameters)
        return response