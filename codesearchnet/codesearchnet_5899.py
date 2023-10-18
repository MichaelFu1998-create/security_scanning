def update(self, store_id, data):
        """
        Update a store.

        :param store_id: The store id.
        :type store_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        """
        self.store_id = store_id
        return self._mc_client._patch(url=self._build_path(store_id), data=data)