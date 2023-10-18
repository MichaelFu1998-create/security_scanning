def all(self, list_id, **queryparams):
        """
        returns the first 10 segments for a specific list.
        """
        return self._mc_client._get(url=self._build_path(list_id, 'segments'), **queryparams)