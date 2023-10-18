def update_members(self, list_id, segment_id, data):
        """
        Batch add/remove list members to static segment.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param segment_id: The unique id for the segment.
        :type segment_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "members_to_add": array,
            "members_to_remove": array
        }
        """
        self.list_id = list_id
        self.segment_id = segment_id
        return self._mc_client._post(url=self._build_path(list_id, 'segments', segment_id), data=data)