def end(self, *args, **kwargs):
        """
        Writes the passed chunk, flushes it to the client,
        and terminates the connection.
        """
        self.send(*args, **kwargs)
        self.close()