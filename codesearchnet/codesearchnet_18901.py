def create_link(self, token, folder_id, url, **kwargs):
        """
        Create a link bitstream.

        :param token: A valid token for the user in question.
        :type token: string
        :param folder_id: The id of the folder in which to create a new item
            that will contain the link. The new item will have the same name as
            the URL unless an item name is supplied.
        :type folder_id: int | long
        :param url: The URL of the link you will create, will be used as the
            name of the bitstream and of the item unless an item name is
            supplied.
        :type url: string
        :param item_name: (optional)  The name of the newly created item, if
            not supplied, the item will have the same name as the URL.
        :type item_name: string
        :param length: (optional) The length in bytes of the file to which the
            link points.
        :type length: int | long
        :param checksum: (optional) The MD5 checksum of the file to which the
            link points.
        :type checksum: string
        :returns: The item information of the item created.
        :rtype: dict
        """
        parameters = dict()
        parameters['token'] = token
        parameters['folderid'] = folder_id
        parameters['url'] = url
        optional_keys = ['item_name', 'length', 'checksum']
        for key in optional_keys:
            if key in kwargs:
                if key == 'item_name':
                    parameters['itemname'] = kwargs[key]
                    continue
                parameters[key] = kwargs[key]
        response = self.request('midas.link.create', parameters)
        return response