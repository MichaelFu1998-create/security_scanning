def create_item(self, token, name, parent_id, **kwargs):
        """
        Create an item to the server.

        :param token: A valid token for the user in question.
        :type token: string
        :param name: The name of the item to be created.
        :type name: string
        :param parent_id: The id of the destination folder.
        :type parent_id: int | long
        :param description: (optional) The description text of the item.
        :type description: string
        :param uuid: (optional) The UUID for the item. It will be generated if
            not given.
        :type uuid: string
        :param privacy: (optional) The privacy state of the item
            ('Public' or 'Private').
        :type privacy: string
        :returns: Dictionary containing the details of the created item.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['name'] = name
        parameters['parentid'] = parent_id
        optional_keys = ['description', 'uuid', 'privacy']
        for key in optional_keys:
            if key in kwargs:
                parameters[key] = kwargs[key]
        response = self.request('midas.item.create', parameters)
        return response