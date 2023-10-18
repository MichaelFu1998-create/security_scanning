def get(self, list_id, merge_id):
        """
        Get information about a specific merge field in a list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param merge_id: The id for the merge field.
        :type merge_id: :py:class:`str`
        """
        self.list_id = list_id
        self.merge_id = merge_id
        return self._mc_client._get(url=self._build_path(list_id, 'merge-fields', merge_id))