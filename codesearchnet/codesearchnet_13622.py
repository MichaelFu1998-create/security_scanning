def send_stream_tail(self):
        """
        Send stream tail via the transport.
        """
        with self.lock:
            if not self._socket or self._hup:
                logger.debug(u"Cannot send stream closing tag: already closed")
                return
            data = self._serializer.emit_tail()
            try:
                self._write(data.encode("utf-8"))
            except (IOError, SystemError, socket.error), err:
                logger.debug(u"Sending stream closing tag failed: {0}"
                                                                .format(err))
            self._serializer = None
            self._hup = True
            if self._tls_state is None:
                try:
                    self._socket.shutdown(socket.SHUT_WR)
                except socket.error:
                    pass
            self._set_state("closing")
            self._write_queue.clear()
            self._write_queue_cond.notify()