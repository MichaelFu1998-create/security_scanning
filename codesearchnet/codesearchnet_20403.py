def close(self):
        """Flush and close the stream.

        This is called automatically by the base resource on resources
        unless the resource is operating asynchronously; in that case,
        this method MUST be called in order to signal the end of the request.
        If not the request will simply hang as it is waiting for some
        thread to tell it to return to the client.
        """

        # Ensure we're not closed.
        self.require_not_closed()

        if not self.streaming or self.asynchronous:
            # We're not streaming, auto-write content-length if not
            # already set.
            if 'Content-Length' not in self.headers:
                self.headers['Content-Length'] = self.tell()

        # Flush out the current buffer.
        self.flush()

        # We're done with the response; inform the HTTP connector
        # to close the response stream.
        self._closed = True