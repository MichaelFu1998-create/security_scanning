def _feed_reader(self, data):
        """Feed the stream reader with data received.

        [ called with `lock` acquired ]

        If `data` is None or empty, then stream end (peer disconnected) is
        assumed and the stream is closed.

        `lock` is acquired during the operation.

        :Parameters:
            - `data`: data received from the stream socket.
        :Types:
            - `data`: `unicode`
        """
        IN_LOGGER.debug("IN: %r", data)
        if data:
            self.lock.release() # not to deadlock with the stream
            try:
                self._reader.feed(data)
            finally:
                self.lock.acquire()
        else:
            self._eof = True
            self.lock.release() # not to deadlock with the stream
            try:
                self._stream.stream_eof()
            finally:
                self.lock.acquire()
            if not self._serializer:
                if self._state != "closed":
                    self.event(DisconnectedEvent(self._dst_addr))
                    self._set_state("closed")