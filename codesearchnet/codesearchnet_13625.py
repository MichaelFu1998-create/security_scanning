def is_readable(self):
        """
        :Return: `True` when the I/O channel can be read
        """
        return self._socket is not None and not self._eof and (
                    self._state in ("connected", "closing")
                        or self._state == "tls-handshake"
                                        and self._tls_state == "want_read")