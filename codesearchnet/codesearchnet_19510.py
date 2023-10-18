def next_chunk_boundaries_levels(self, buf, prepend_bytes=0):
        """Computes the next chunk boundaries within `buf`.

        Similar to :meth:`.next_chunk_boundaries`, but information about which chunker led to a respective boundary is
        included in the returned value.

        Args:
            buf (bytes): The message that is to be chunked.
            prepend_bytes (Optional[int]): Optional number of zero bytes that should be input to the chunking algorithm
                before `buf`.

        Returns:
            list: List of tuples (boundary, level), where boundary is a boundary position relative to `buf` and level is
                the index of the chunker (i.e., the index of its chunk size specified during instantiation) that yielded
                the boundary.

            If multiple chunkers yield the same boundary, it is returned only once, along with the highest matching
            chunker index.
        """
        boundaries = {}
        for level_index, chunker in enumerate(self._chunkers):
            boundaries.update(
                dict([(boundary, level_index) for boundary in chunker.next_chunk_boundaries(buf, prepend_bytes)]))
        return sorted(boundaries.items())