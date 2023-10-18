def send(self, *args, **kwargs):
        """Writes the passed chunk and flushes it to the client."""
        self.write(*args, **kwargs)
        self.flush()