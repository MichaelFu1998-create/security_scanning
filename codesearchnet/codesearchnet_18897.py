def move_item(self, token, item_id, src_folder_id, dest_folder_id):
        """
        Move an item from the source folder to the destination folder.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the item to be moved
        :type item_id: int | long
        :param src_folder_id: The id of source folder where the item is located
        :type src_folder_id: int | long
        :param dest_folder_id: The id of destination folder where the item is
            moved to
        :type dest_folder_id: int | long
        :returns: Dictionary containing the details of the moved item
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['id'] = item_id
        parameters['srcfolderid'] = src_folder_id
        parameters['dstfolderid'] = dest_folder_id
        response = self.request('midas.item.move', parameters)
        return response