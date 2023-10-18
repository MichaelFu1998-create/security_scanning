def create_chunker(self, chunk_size):
        """Create a chunker performing content-defined chunking (CDC) using Rabin Karp's rolling hash scheme with a
        specific, expected chunk size.

        Args:
            chunk_size (int): (Expected) target chunk size.

        Returns:
            BaseChunker: A chunker object.
        """
        rolling_hash = _rabinkarprh.RabinKarpHash(self.window_size, self._seed)
        rolling_hash.set_threshold(1.0 / chunk_size)
        return RabinKarpCDC._Chunker(rolling_hash)