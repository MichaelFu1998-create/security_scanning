def create_multilevel_chunker(self, chunk_sizes):
        """Create a multi-level chunker performing content-defined chunking (CDC) using Rabin Karp's rolling hash scheme
        with different specific, expected chunk sizes.

        Args:
            chunk_sizes (list): List of (expected) target chunk sizes.

                Warning:
                    For performance reasons, behavior is only defined if chunk sizes are passed in order, i.e., from
                    lowest to highest value.

        Returns:
            BaseMultiLevelChunker: A multi-level chunker object.
        """
        rolling_hash = _rabinkarprh.RabinKarpMultiThresholdHash(self.window_size, self._seed,
                                                                [1.0 / chunk_size for chunk_size in chunk_sizes])
        return RabinKarpCDC._MultiLevelChunker(rolling_hash)