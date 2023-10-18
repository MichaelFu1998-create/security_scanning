def create(self, data):
        """
        Upload a new image or file to the File Manager.

        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*,
            "file_data": string*
        }
        """
        if 'name' not in data:
            raise KeyError('The file must have a name')
        if 'file_data' not in data:
            raise KeyError('The file must have file_data')
        response = self._mc_client._post(url=self._build_path(), data=data)
        if response is not None:
            self.file_id = response['id']
        else:
            self.file_id = None
        return response