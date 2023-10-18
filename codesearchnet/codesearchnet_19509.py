def next_chunk_boundaries(self, buf, prepend_bytes=0):
        """Computes the next chunk boundaries within `buf`.

        See :meth:`.BaseChunker.next_chunk_boundaries`.
        """
        return (boundary for boundary, _ in self.next_chunk_boundaries_levels(buf, prepend_bytes))