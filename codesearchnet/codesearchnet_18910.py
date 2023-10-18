def create_small_thumbnail(self, token, item_id):
        """
        Create a 100x100 small thumbnail for the given item. It is used for
        preview purpose and displayed in the 'preview' and 'thumbnails'
        sidebar sections.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The item on which to set the thumbnail.
        :type item_id: int | long
        :returns: The item object (with the new thumbnail id) and the path
            where the newly created thumbnail is stored.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['itemId'] = item_id
        response = self.request(
            'midas.thumbnailcreator.create.small.thumbnail', parameters)
        return response