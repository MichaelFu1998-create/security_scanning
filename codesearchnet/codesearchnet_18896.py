def share_item(self, token, item_id, dest_folder_id):
        """
        Share an item to the destination folder.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the item to be shared.
        :type item_id: int | long
        :param dest_folder_id: The id of destination folder where the item is
            shared to.
        :type dest_folder_id: int | long
        :returns: Dictionary containing the details of the shared item.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = item_id
        parameters['dstfolderid'] = dest_folder_id
        response = self.request('midas.item.share', parameters)
        return response