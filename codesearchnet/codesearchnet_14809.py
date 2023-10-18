def _chunks(self, iterable, chunk_size):
        """Chunks data into chunk with size<=chunk_size."""
        iterator = iter(iterable)
        chunk = list(itertools.islice(iterator, 0, chunk_size))
        while chunk:
            yield chunk
            chunk = list(itertools.islice(iterator, 0, chunk_size))