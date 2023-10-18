def update(self, folder_id, data):
        """
        Update a specific folder used to organize templates.

        :param folder_id: The unique id for the File Manager folder.
        :type folder_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*
        }
        """
        if 'name' not in data:
            raise KeyError('The template folder must have a name')
        self.folder_id = folder_id
        return self._mc_client._patch(url=self._build_path(folder_id), data=data)