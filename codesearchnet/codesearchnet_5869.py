def create(self, list_id, data):
        """
        adds a new segment to the list.
        """
        return self._mc_client._post(url=self._build_path(list_id, 'segments'), data=data)