def set_target(self, stream):
        """Make the `stream` the target for this transport instance.

        The 'stream_start', 'stream_end' and 'stream_element' methods
        of the target will be called when appropriate content is received.

        :Parameters:
            - `stream`: the stream handler to receive stream content
              from the transport
        :Types:
            - `stream`: `StreamBase`
        """
        with self.lock:
            if self._stream:
                raise ValueError("Target stream already set")
            self._stream = stream
            self._reader = StreamReader(stream)