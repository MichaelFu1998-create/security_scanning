def set_item_metadata(self, token, item_id, element, value,
                          qualifier=None):
        """
        Set the metadata associated with an item.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the item for which metadata will be set.
        :type item_id: int | long
        :param element: The metadata element name.
        :type element: string
        :param value: The metadata value for the field.
        :type value: string
        :param qualifier: (optional) The metadata qualifier. Defaults to empty
            string.
        :type qualifier: None | string
        :returns: None.
        :rtype: None
        """
        parameters = dict()
        parameters['token'] = token
        parameters['itemId'] = item_id
        parameters['element'] = element
        parameters['value'] = value
        if qualifier:
            parameters['qualifier'] = qualifier
        response = self.request('midas.item.setmetadata', parameters)
        return response