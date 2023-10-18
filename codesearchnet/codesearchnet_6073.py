def read(self, size=None):
        """Read bytes from an iterator."""
        while size is None or len(self.buffer) < size:
            try:
                self.buffer += next(self.data_stream)
            except StopIteration:
                break

        sized_chunk = self.buffer[:size]
        if size is None:
            self.buffer = ""
        else:
            self.buffer = self.buffer[size:]
        return sized_chunk