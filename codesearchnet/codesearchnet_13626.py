def wait_for_readability(self):
        """
        Stop current thread until the channel is readable.

        :Return: `False` if it won't be readable (e.g. is closed)
        """
        with self.lock:
            while True:
                if self._socket is None or self._eof:
                    return False
                if self._state in ("connected", "closing"):
                    return True
                if self._state == "tls-handshake" and \
                                            self._tls_state == "want_read":
                    return True
                self._state_cond.wait()