def _build_chunk_headers(self):
        """ Build headers for each field. """
        if hasattr(self, "_chunk_headers") and self._chunk_headers:
            return

        self._chunk_headers = {}
        for field in self._files:
            self._chunk_headers[field] = self._headers(field, True)
        for field in self._data:
            self._chunk_headers[field] = self._headers(field)