def delete(self, list_id, segment_id):
        """
        removes an existing list segment from the list. This cannot be undone.
        """
        return self._mc_client._delete(url=self._build_path(list_id, 'segments', segment_id))