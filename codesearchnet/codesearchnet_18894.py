def get_item_metadata(self, item_id, token=None, revision=None):
        """
        Get the metadata associated with an item.

        :param item_id: The id of the item for which metadata will be returned
        :type item_id: int | long
        :param token: (optional) A valid token for the user in question.
        :type token: None | string
        :param revision: (optional) Revision of the item. Defaults to latest
            revision.
        :type revision: int | long
        :returns: List of dictionaries containing item metadata.
        :rtype: list[dict]
        """
        parameters = dict()
        parameters['id'] = item_id
        if token:
            parameters['token'] = token
        if revision:
            parameters['revision'] = revision
        response = self.request('midas.item.getmetadata', parameters)
        return response