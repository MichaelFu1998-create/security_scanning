def disconnect(self):
        """Disconnect the stream gracefully."""
        logger.debug("TCPTransport.disconnect()")
        with self.lock:
            if self._socket is None:
                if self._state != "closed":
                    self.event(DisconnectedEvent(self._dst_addr))
                    self._set_state("closed")
                return
            if self._hup or not self._serializer:
                self._close()
            else:
                self.send_stream_tail()