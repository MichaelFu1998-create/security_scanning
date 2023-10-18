def _length(self):
        """ Returns total length for this request.

        Returns:
            int. Length
        """
        self._build_chunk_headers()

        length = 0

        if self._data:
            for field in self._data:
                length += len(self._chunk_headers[field])
                length += len(self._data[field])
                length += 2

        if self._files:
            for field in self._files:
                length += len(self._chunk_headers[field])
                length += self._file_size(field)
                length += 2

        length += len(self.boundary)
        length += 6

        return length