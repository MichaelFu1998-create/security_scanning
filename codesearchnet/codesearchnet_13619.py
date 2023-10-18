def _write(self, data):
        """Write raw data to the socket.

        :Parameters:
            - `data`: data to send
        :Types:
            - `data`: `bytes`
        """
        OUT_LOGGER.debug("OUT: %r", data)
        if self._hup or not self._socket:
            raise PyXMPPIOError(u"Connection closed.")
        try:
            while data:
                try:
                    sent = self._socket.send(data)
                except ssl.SSLError, err:
                    if err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                        continue
                    else:
                        raise
                except socket.error, err:
                    if err.args[0] == errno.EINTR:
                        continue
                    if err.args[0] in BLOCKING_ERRORS:
                        wait_for_write(self._socket)
                        continue
                    raise
                data = data[sent:]
        except (IOError, OSError, socket.error), err:
            raise PyXMPPIOError(u"IO Error: {0}".format(err))