def update(self, file_id, data):
        """
        Update a file in the File Manager.

        :param file_id: The unique id for the File Manager file.
        :type file_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*,
            "file_data": string*
        }
        """
        self.file_id = file_id
        if 'name' not in data:
            raise KeyError('The file must have a name')
        if 'file_data' not in data:
            raise KeyError('The file must have file_data')
        return self._mc_client._patch(url=self._build_path(file_id), data=data)