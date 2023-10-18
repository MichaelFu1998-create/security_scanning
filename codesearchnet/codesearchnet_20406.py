def flush(self):
        """Flush the write buffers of the stream.

        This results in writing the current contents of the write buffer to
        the transport layer, initiating the HTTP/1.1 response. This initiates
        a streaming response. If the `Content-Length` header is not given
        then the chunked `Transfer-Encoding` is applied.
        """

        # Ensure we're not closed.
        self.require_not_closed()

        # Pull out the accumulated chunk.
        chunk = self._stream.getvalue()
        self._stream.truncate(0)
        self._stream.seek(0)

        # Append the chunk to the body.
        self.body = chunk if (self._body is None) else (self._body + chunk)

        if self.asynchronous:
            # We are now streaming because we're asynchronous.
            self.streaming = True