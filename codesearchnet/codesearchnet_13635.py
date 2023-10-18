def handle_err(self):
        """
        Handle an error reported.
        """
        with self.lock:
            if self._state == 'connecting' and self._dst_addrs:
                self._hup = False
                self._set_state("connect")
                return
            self._socket.close()
            self._socket = None
            self._set_state("aborted")
            self._write_queue.clear()
            self._write_queue_cond.notify()
        raise PyXMPPIOError("Unhandled error on socket")