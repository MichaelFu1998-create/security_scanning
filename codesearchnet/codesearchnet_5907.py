def update(self, list_id, segment_id, data):
        """
        Update a specific segment in a list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param segment_id: The unique id for the segment.
        :type segment_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*
        }
        """
        self.list_id = list_id
        self.segment_id = segment_id
        if 'name' not in data:
            raise KeyError('The list segment must have a name')
        return self._mc_client._patch(url=self._build_path(list_id, 'segments', segment_id), data=data)