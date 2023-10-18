def get(self, list_id, segment_id):
        """
        returns the specified list segment.
        """
        return self._mc_client._get(url=self._build_path(list_id, 'segments', segment_id))