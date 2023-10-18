def create(self, list_id, data):
        """
        Add a new merge field for a specific list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*,
            "type": string*
        }
        """
        self.list_id = list_id
        if 'name' not in data:
            raise KeyError('The list merge field must have a name')
        if 'type' not in data:
            raise KeyError('The list merge field must have a type')
        response = self._mc_client._post(url=self._build_path(list_id, 'merge-fields'), data=data)
        if response is not None:
            self.merge_id = response['merge_id']
        else:
            self.merge_id = None
        return response