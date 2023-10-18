def handle_read(self):
        """
        Handle the 'channel readable' state. E.g. read from a socket.
        """
        with self.lock:
            logger.debug("handle_read()")
            if self._eof or self._socket is None:
                return
            if self._state == "tls-handshake":
                while True:
                    logger.debug("tls handshake read...")
                    self._continue_tls_handshake()
                    logger.debug("  state: {0}".format(self._tls_state))
                    if self._tls_state != "want_read":
                        break
            elif self._tls_state == "connected":
                while self._socket and not self._eof:
                    logger.debug("tls socket read...")
                    try:
                        data = self._socket.read(4096)
                    except ssl.SSLError, err:
                        if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                            break
                        elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                            break
                        else:
                            raise
                    except socket.error, err:
                        if err.args[0] == errno.EINTR:
                            continue
                        elif err.args[0] in BLOCKING_ERRORS:
                            break
                        elif err.args[0] == errno.ECONNRESET:
                            logger.warning("Connection reset by peer")
                            data = None
                        else:
                            raise
                    self._feed_reader(data)
            else:
                while self._socket and not self._eof:
                    logger.debug("raw socket read...")
                    try:
                        data = self._socket.recv(4096)
                    except socket.error, err:
                        if err.args[0] == errno.EINTR:
                            continue
                        elif err.args[0] in BLOCKING_ERRORS:
                            break
                        elif err.args[0] == errno.ECONNRESET:
                            logger.warning("Connection reset by peer")
                            data = None
                        else:
                            raise
                    self._feed_reader(data)