def update(self, list_id, segment_id, data):
        """
        updates an existing list segment.
        """
        return self._mc_client._patch(url=self._build_path(list_id, 'segments', segment_id), data=data)