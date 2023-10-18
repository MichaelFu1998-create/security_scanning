def associate_item_with_scalar_data(self, token, item_id, scalar_id,
                                        label):
        """
        Associate a result item with a particular scalar value.

        :param token: A valid token for the user in question.
        :type token: string
        :param item_id: The id of the item to associate with the scalar.
        :type item_id: int | long
        :param scalar_id: Scalar id with which to associate the item.
        :type scalar_id: int | long
        :param label: The label describing the nature of the association.
        :type label: string
        """
        parameters = dict()
        parameters['token'] = token
        parameters['scalarIds'] = scalar_id
        parameters['itemId'] = item_id
        parameters['label'] = label
        self.request('midas.tracker.item.associate', parameters)