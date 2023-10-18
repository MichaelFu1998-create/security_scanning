def _close(self):
        """Same as `_close` but expects `lock` acquired.
        """
        if self._state != "closed":
            self.event(DisconnectedEvent(self._dst_addr))
            self._set_state("closed")
        if self._socket is None:
            return
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self._socket.close()
        self._socket = None
        self._write_queue.clear()
        self._write_queue_cond.notify()